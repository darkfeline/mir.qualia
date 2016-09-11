import collections
import re


class Qualifier:

    _BEGIN_PATTERN = re.compile(r'^(?P<prefix>\S+)\s+BEGIN\s+(?P<quality>\S+)')

    def __init__(self, qualities):
        self.qualities = qualities

    def __repr__(self):
        return '{cls}(qualities={this.qualities!r})}'.format(
            cls=type(self).__qualname__, this=self)

    def __call__(self, lines):
        processor = self._processer()
        self._queue = queue = IteratorQueue()
        for line in lines:
            processor.send(line)
            yield from queue

    def _processor(self):
        begin_pattern = self._BEGIN_PATTERN
        while True:
            line = yield
            match = begin_pattern.search(line)
            if match is None:
                self._queue.extend([line])
            else:
                attrs = _BlockAttributes(
                    match.group('prefix', 'quality'))
                yield from self._process_qualified_block(attrs)

    def _process_qualified_block(self, attrs):
        block_lines = []
        pattern = re.compile(r'{attrs.prefix}\s+END\s+{attrs.quality}'.format(
            attrs=attrs))
        while True:
            line = yield
            match = pattern.search(line)
            if match is None:
                block_lines.append(line)
            else:
                self._close_qualified_block(attrs, block_lines)
                break

    def _close_qualified_block(self, attrs, block_lines):
        prefix = CommentPrefix(attrs.prefix)
        if attrs.quality in self.qualities:
            self._queue.extend(prefix.uncomment(block_lines))
        else:
            self._queue.extend(prefix.comment(block_lines))


_BlockAttributes = collections.namedtuple(
    '_BlockAttributes', 'prefix quality')


class IteratorQueue:

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

    def extend(self, iterable):
        self.queue.extend(iterable)


class CommentPrefix:

    """Comments and uncomments lines, given a prefix.

    >>> prefix = CommentPrefix('#')
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
        self._prefix_pattern = re.compile(r'^{}\s*'.format(comment_prefix))

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
