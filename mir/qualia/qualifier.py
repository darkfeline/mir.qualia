# Copyright (C) 2016 Allen Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import re

from mir.qualia.indent import common_indent

logger = logging.getLogger(__name__)


class Qualifier:

    """Qualify lines.

    A Qualifier takes lines of text that may contain qualified blocks of the
    form:

       # BEGIN quality_name
       lines in block
       # END quality_name

    and either comments or uncomments the contents of the blocks depending on
    the qualities of the Qualifier instance.

    Qualifier is implemented as a generator, so processing is done lazily.
    """

    _BEGIN_PATTERN = re.compile(
        r'^\s*(?P<prefix>\S+)\s*BEGIN\s+(?P<quality>\S+)')
    _EOF = object()

    def __init__(self, qualities):
        self.qualities = qualities

    def __repr__(self):
        return '{cls}(qualities={this.qualities!r})'.format(
            cls=type(self).__qualname__, this=self)

    def __call__(self, lines):
        """Qualify lines.

        `lines` is an iterable of strings.
        """
        lines = iter(lines)
        from_begin_line = _BlockAttributes.from_begin_line
        for line in lines:
            logger.debug('Yielding line %r', line)
            yield line
            block_attrs = from_begin_line(line)
            if block_attrs:
                logger.debug('Entering block')
                yield from self._qualify_block(block_attrs, lines)

    def _qualify_block(self, attrs, rest):
        """Qualify lines in a block.

        `attrs` is a _BlockAttributes instance.  `rest` is an iterator of
        remaining lines.
        """
        block_lines = []
        is_end_line = attrs.is_end_line
        for line in rest:
            if is_end_line(line):
                yield from self._close_qualified_block(attrs, block_lines)
                logger.debug('Yielding %r', line)
                yield line
                break
            else:
                logger.debug('Queuing line %r', line)
                block_lines.append(line)
        else:
            # We reached EOF without seeing an end line (an incomplete block).
            # We dump all the lines that we were holding without extra
            # processing.
            logger.debug('Reached end, dumping lines')
            yield from block_lines

    def _close_qualified_block(self, attrs, block_lines):
        """Emit the lines of the parse qualified block according to qualities.

        Args:
            attrs: A _BlockAttributes instance.
            block_lines: A sequence of lines inside the block.
        """
        if attrs.quality in self.qualities:
            yield from attrs.comment_prefix.uncomment(block_lines)
        else:
            yield from attrs.comment_prefix.comment(block_lines)


class _BlockAttributes:

    """Attributes for a qualified block.

    `prefix` is the comment prefix preceding the BEGIN and END keywords.
    `quality` is the quality name for the block.
    """

    __slots__ = ('prefix', 'quality', '_end_pattern')
    _BEGIN = r'^\s*(?P<prefix>\S+)\s*BEGIN\s+(?P<quality>\S+)'
    _END = r'^\s*{prefix}\s*END\s+{quality}'
    _BEGIN_PATTERN = re.compile(_BEGIN)

    def __init__(self, prefix, quality):
        self.prefix = prefix
        self.quality = quality
        self._end_pattern = re.compile(
            self._END.format(prefix=re.escape(prefix),
                             quality=re.escape(quality)))

    def __repr__(self):
        return ('{cls}(prefix={this.prefix!r}, quality={this.quality!r})'
                .format(
                    cls=type(self).__qualname__,
                    this=self))

    @classmethod
    def from_begin_line(cls, line):
        """Instantiate an instance from a begin line.

        Return None if the line isn't a begin line.
        """
        match = cls._BEGIN_PATTERN.search(line)
        if match:
            return cls(*match.group('prefix', 'quality'))
        else:
            return None

    def is_end_line(self, line):
        """Return a true value if line is an end line for this block."""
        return self._end_pattern.search(line)

    @property
    def comment_prefix(self):
        """Return a _CommentPrefix instance corresponding to this block."""
        return _CommentPrefix(self.prefix)


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

    def __init__(self, comment_prefix):
        self.comment_prefix = comment_prefix
        self._prefix_pattern = re.compile(
            r'^(?P<indent>\s*)' + re.escape(comment_prefix))

    def __repr__(self):
        return '{cls}({this.comment_prefix!r})'.format(
            cls=type(self).__qualname__, this=self)

    def is_commented(self, lines):
        """Return True if all lines are commented."""
        pattern = self._prefix_pattern
        return all(pattern.search(line) for line in lines)

    def uncomment(self, lines):
        r"""Uncomment a sequence of lines.

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
        if not lines:
            return []
        while self.is_commented(lines):
            lines = self._uncomment(lines)
        return lines

    def _uncomment(self, lines):
        """Unconditionally uncomment a sequence of lines once."""
        return [self._prefix_pattern.sub(r'\g<indent>', line)
                for line in lines]

    def comment(self, lines):
        """Comment a sequence of lines."""
        if not self.is_commented(lines):
            return self._comment(lines)
        return lines

    def _comment(self, lines):
        """Unconditionally comment a sequence of lines."""
        indent = common_indent(lines)
        indent_len = len(indent)
        prefix = self.comment_prefix
        return [indent + prefix + line[indent_len:] for line in lines]
