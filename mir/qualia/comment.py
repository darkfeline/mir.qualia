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

"""Comment and uncomment lines.

Classes:
CommentPrefix
"""

import re

from mir.qualia.indent import common_indent


class CommentPrefix:

    r"""Comments and uncomments lines, given a prefix.

    >>> prefix = CommentPrefix('#')
    >>> prefix.uncomment(['#export EDITOR=vi\n'])
    ['export EDITOR=vi\n']
    >>> prefix.comment(['export EDITOR=vi\n'])
    ['#export EDITOR=vi\n']
    >>> prefix.is_commented(['export EDITOR=vi\n'])
    False

    Do not modify the comment_prefix attribute on an instance.
    """

    def __init__(self, comment_prefix):
        self._comment_prefix = comment_prefix
        self._prefix_pattern = re.compile(
            fr'^(?P<indent>\s*){re.escape(comment_prefix)}')

    def __repr__(self):
        cls = type(self).__qualname__
        return f'{cls}({self._comment_prefix!r})'

    def is_commented(self, lines):
        """Return True if all lines are commented."""
        pattern = self._prefix_pattern
        return all(pattern.search(line) for line in lines)

    def uncomment(self, lines):
        r"""Uncomment a sequence of lines.

        This will keep uncommenting so long as the lines are all commented.
        This is so that uncommenting is an idempotent operation.

        >>> prefix = CommentPrefix('#')
        >>> prefix.uncomment(['##foo\n', '##bar\n'])
        ['foo\n', 'bar\n']
        >>> prefix.uncomment(prefix.uncomment(['##foo\n', '##bar\n']))
        ['foo\n', 'bar\n']

        In almost all cases, this is desired behavior, but if you need to
        preserve levels of commenting, include a line to protect them:

        >>> prefix = CommentPrefix('#')
        >>> prefix.uncomment(['##foo\n', '##bar\n', '#\n'])
        ['#foo\n', '#bar\n', '\n']
        """
        if not lines:
            return []
        while self.is_commented(lines):
            lines = self._force_uncomment(lines)
        return lines

    def _force_uncomment(self, lines):
        """Unconditionally uncomment a sequence of lines once."""
        return [self._prefix_pattern.sub(r'\g<indent>', line)
                for line in lines]

    def comment(self, lines):
        """Comment a sequence of lines."""
        if not self.is_commented(lines):
            return self._force_comment(lines)
        return lines

    def _force_comment(self, lines):
        """Unconditionally comment a sequence of lines."""
        indent = common_indent(lines)
        indent_len = len(indent)
        prefix = self._comment_prefix
        return [f'{indent}{prefix}{line[indent_len:]}' for line in lines]
