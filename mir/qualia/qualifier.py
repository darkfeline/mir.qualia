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

from mir.qualia.comment import CommentPrefix

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

    def __init__(self, qualities):
        self._qualities = qualities

    def __repr__(self):
        cls = type(self).__qualname__
        return f'{cls}(qualities={self._qualities!r})'

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
        prefix = attrs.get_comment_prefix()
        if attrs.is_active(self._qualities):
            yield from prefix.uncomment(block_lines)
        else:
            yield from prefix.comment(block_lines)


class _BlockAttributes:

    """Attributes for a qualified block.

    `prefix` is the comment prefix preceding the BEGIN and END keywords.
    `quality` is the quality name for the block.
    """

    __slots__ = ('_prefix', '_quality', '_end_pattern')
    _BEGIN = r'^\s*(?P<prefix>\S+)\s*BEGIN\s+(?P<quality>\S+)'
    _END = r'^\s*{prefix}\s*END\s+{quality}'
    _BEGIN_PATTERN = re.compile(_BEGIN)

    def __init__(self, prefix, quality):
        self._prefix = prefix
        self._quality = quality
        self._end_pattern = re.compile(
            self._END.format(prefix=re.escape(prefix),
                             quality=re.escape(quality)))

    def __repr__(self):
        cls = type(self).__qualname__
        return f'{cls}(prefix={self._prefix!r}, quality={self._quality!r})'

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

    def is_active(self, qualities):
        """Return whether the block is active under the given qualities."""
        return self._quality in qualities

    def get_comment_prefix(self):
        """Return a CommentPrefix instance corresponding to this block."""
        return CommentPrefix(self._prefix)
