"""qualifier module.


"""

import collections
import functools
import itertools
import re


class Qualifier:

    """Qualify lines.

    A Qualifier takes lines of text that may contain qualified blocks of the form::

       # BEGIN quality_name
       lines in block
       # END quality_name

    and either comments or uncomments the contents of the blocks depending on
    the qualities of the Qualifier instance.

    Qualifier is implemented as a generator, so processing is done lazily.

    """

    _BEGIN_PATTERN = re.compile(r'^(?P<prefix>\S+)\s+BEGIN\s+(?P<quality>\S+)')
    _EOF = object()

    def __init__(self, qualities):
        self.qualities = qualities

    def __repr__(self):
        return '{cls}(qualities={this.qualities!r})}'.format(
            cls=type(self).__qualname__, this=self)

    def __call__(self, lines):
        processor = self._processor()
        next(processor)
        self._output_queue = output_queue = _IteratorQueue()
        for line in itertools.chain(lines, [self._EOF]):
            processor.send(line)
            yield from output_queue

    def _processor(self):
        """State machine coroutine.

        This implements the state machine for parsing and transforming
        qualified blocks using coroutines.

        """
        while True:
            line = yield
            if line is self._EOF:
                break
            else:
                yield from self._process_line(line)

    def _process_line(self, line):
        """Process single line in the normal state."""
        self._output_queue.append(line)
        match = self._BEGIN_PATTERN.search(line)
        if match:
            attrs = _BlockAttributes(*match.group('prefix', 'quality'))
            yield from self._process_qualified_block(attrs)

    def _process_qualified_block(self, attrs):
        """Process lines in a qualified block.

        Args:
            attrs: A _BlockAttributes instance.

        """
        block_lines = []
        pattern = self._get_end_pattern(attrs)
        while True:
            line = yield
            if line is self._EOF:
                self._output_queue.extend(block_lines)
                break
            else:
                match = pattern.search(line)
                if match is None:
                    block_lines.append(line)
                else:
                    self._close_qualified_block(attrs, block_lines)
                    self._output_queue.append(line)
                    break

    @functools.lru_cache(maxsize=8)
    def _get_end_pattern(self, attrs):
        """Get compiled RE pattern for given block attributes.

        Args:
            attrs: A _BlockAttributes instance.

        """
        return re.compile(r'{attrs.prefix}\s+END\s+{attrs.quality}'.format(
            attrs=attrs))

    def _close_qualified_block(self, attrs, block_lines):
        """Emit the lines of the parse qualified block according to qualities.

        Args:
            attrs: A _BlockAttributes instance.
            block_lines: A list of strings, the lines inside the block.

        """
        prefix = _CommentPrefix(attrs.prefix)
        if attrs.quality in self.qualities:
            self._output_queue.extend(prefix.uncomment(block_lines))
        else:
            self._output_queue.extend(prefix.comment(block_lines))


_BlockAttributes = collections.namedtuple(
    '_BlockAttributes', 'prefix quality')


class _IteratorQueue:

    """A queue that accessed via iteration."""

    def __init__(self, iterable=()):
        self.queue = collections.deque(iterable)

    def __repr__(self):
        return '<{cls} id=0x{id:x} queue={queue!r}>'.format(
            cls=type(self).__qualname__,
            id=id(self),
            queue=self.queue)

    def __iter__(self):
        return self

    def __next__(self):
        if self.queue:
            return self.queue.popleft()
        else:
            raise StopIteration

    def append(self, obj):
        """Add object to the queue."""
        self.queue.append(obj)

    def extend(self, iterable):
        """Add objects in the given iterable to the queue."""
        self.queue.extend(iterable)


class _CommentPrefix:

    """Comments and uncomments lines, given a prefix.

    >>> prefix = _CommentPrefix('#')
    >>> prefix.uncomment(['#export EDITOR=vi'])
    ['export EDITOR=vi']
    >>> prefix.comment(['export EDITOR=vi'])
    ['#export EDITOR=vi']
    >>> prefix.is_commented(['export EdITOR=vi'])
    False

    Do not modify the comment_prefix attribute on an instance.

    """

    def __init__(self, comment_prefix):
        self.comment_prefix = comment_prefix
        self._prefix_pattern = re.compile(r'^{}'.format(comment_prefix))

    def __str__(self):
        return self.comment_prefix

    def __repr__(self):
        return '{cls}({this.comment_prefix!r})'.format(
            cls=type(self).__qualname__, this=self)

    def is_commented(self, lines):
        """Return True if all lines are commented."""
        pattern = self._prefix_pattern
        return all(pattern.search(line) for line in lines)

    def uncomment(self, lines):
        """Uncomment lines."""
        pattern = self._prefix_pattern
        while self.is_commented(lines):
            lines = [pattern.sub('', line) for line in lines]
        return lines

    def comment(self, lines):
        """Comment lines."""
        if not self.is_commented(lines):
            prefix = self.comment_prefix
            lines = [prefix + line for line in lines]
        return lines
