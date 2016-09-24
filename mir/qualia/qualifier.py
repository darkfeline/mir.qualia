import collections
import functools
import itertools
import re


class Qualifier:

    """Qualify lines.

    A Qualifier takes lines of text that may contain qualified blocks of the form:

       # BEGIN quality_name
       lines in block
       # END quality_name

    and either comments or uncomments the contents of the blocks depending on
    the qualities of the Qualifier instance.

    Qualifier is implemented as a generator, so processing is done lazily.

    """

    _BEGIN_PATTERN = re.compile(
        r'^\s*(?P<prefix>\S+)\s+BEGIN\s+(?P<quality>\S+)')
    _EOF = object()

    def __init__(self, qualities):
        self.qualities = qualities

    def __repr__(self):
        return '{cls}(qualities={this.qualities!r})'.format(
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
        pattern = _get_end_pattern(attrs)
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


@functools.lru_cache(maxsize=8)
def _get_end_pattern(attrs):
    """Get compiled RE end pattern for given block attributes.

    Args:
        attrs: A _BlockAttributes instance.

    """
    return re.compile(r'{attrs.prefix}\s+END\s+{attrs.quality}'.format(
        attrs=attrs))


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

    r"""Comments and uncomments lines, given a prefix.

    >>> prefix = _CommentPrefix('#')
    >>> prefix.uncomment(['#export EDITOR=vi\n'])
    ['export EDITOR=vi\n']
    >>> prefix.comment(['export EDITOR=vi\n'])
    ['#export EDITOR=vi\n']
    >>> prefix.is_commented(['export EDITOR=vi\n'])
    False

    Do not modify the comment_prefix attribute on an instance.

    """

    _INDENT_PATTERN = re.compile(r'')

    def __init__(self, comment_prefix):
        self.comment_prefix = comment_prefix
        self._prefix_pattern = re.compile(
            r'^(?P<indent>\s*){}'.format(comment_prefix))

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
        r"""Uncomment lines.

        This will keep uncommenting so long as the lines are all commented.
        This is so that uncommenting is an idempotent operation.

        >>> prefix = _CommentPrefix('#')
        >>> prefix.uncomment(['##foo\n', '##bar\n'])
        ['foo\n', 'bar\n']
        >>> prefix.uncomment(prefix.uncomment(['##foo\n', '##bar\n']))
        ['foo\n', 'bar\n']

        In almost all cases, this is desired behavior, but if you need to
        preserve levels of commenting, include a line to protect them:

        >>> prefix = _CommentPrefix('#')
        >>> prefix.uncomment(['##foo\n', '##bar\n', '#\n'])
        ['#foo\n', '#bar\n', '\n']

        """
        pattern = self._prefix_pattern
        while self.is_commented(lines):
            lines = [pattern.sub(r'\g<indent>', line) for line in lines]
        return lines

    def comment(self, lines):
        """Comment lines."""
        if not self.is_commented(lines):
            indent = _common_indent(lines)
            indent_len = len(indent)
            prefix = self.comment_prefix
            lines = [indent + prefix + line[indent_len:] for line in lines]
        return lines


def _common_indent(lines):
    """Find common indentation of given lines."""
    lines = iter(lines)
    try:
        line = next(lines)
    except StopIteration:
        return ''
    indent = _get_indent(line)
    for line in lines:
        new_indent = _get_indent(line)
        indent = ''.join(_find_common_prefix(indent, new_indent))
    return indent


_INDENT_PATTERN = re.compile(r'^\s*')


def _get_indent(line):
    """Return indentation string of line."""
    return _INDENT_PATTERN.search(line).group(0)


def _find_common_prefix(first, second):
    """Find the common prefix of two iterables."""
    yield from (x[0] for x in
            itertools.takewhile(lambda x: x[0] == x[1],
                                zip(first, second)))
