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

"""Find common indent of a sequence of lines.

Functions:
common_indent
"""

import re


def common_indent(lines):
    """Find common indent of a sequence of lines."""
    if not lines:
        return ''
    finder = _CommonIndentFinder(lines[0])
    for line in lines[1:]:
        finder.feed(line)
    return finder.prefix


class _CommonPrefixFinder:

    """Find common prefix of any number of strings.

    Starting with an initial string, additional strings are fed into a
    _CommonPrefixFinder instance, shortening the common prefix.  The current
    running common prefix is stored in the `prefix` instance attribute.
    """

    def __init__(self, initial):
        """Initialize instance.

        initial is the initial prefix string.
        """
        self.prefix = initial

    def __repr__(self):
        return '{cls}({this.prefix!r})'.format(
            cls=type(self).__qualname__,
            this=self)

    def feed(self, string):
        """Feed another string to find the common prefix of."""
        self.prefix = ''.join(_take_while_eq(self.prefix, string))


def _take_while_eq(first, second):
    """Iterate over two iterables while their values are equal."""
    for x, y in zip(first, second):
        if x == y:
            yield x
        else:
            return


class _CommonIndentFinder(_CommonPrefixFinder):

    """Find the common prefix of any number of strings.

    _CommonPrefixFinder behaves mostly like the superclass, except only strings
    are allowed, and the common prefix is automatically trimmed down to leading
    whitespace (indentation).
    """

    _INDENT_PATTERN = re.compile(r'^\s*')

    @property
    def prefix(self):
        return self.__dict__['prefix']

    @prefix.setter
    def prefix(self, line):
        indent = self._INDENT_PATTERN.search(line).group(0)
        self.__dict__['prefix'] = indent
