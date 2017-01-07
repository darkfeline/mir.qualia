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
    return finder.get_prefix()


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
        self._set_prefix(initial)

    def __repr__(self):
        cls = type(self).__qualname__
        return f'{cls}({self._prefix!r})'

    def feed(self, string):
        """Feed another string to find the common prefix of."""
        self._set_prefix(_find_common_prefix(self._prefix, string))

    def get_prefix(self):
        """Get the current common prefix."""
        return self._prefix

    def _set_prefix(self, value):
        """Set the current common prefix.

        This can be overridden in subclasses to do extra processing.
        """
        self._prefix = value


def _find_common_prefix(first, second):
    """Find the common prefix of two strings."""
    return ''.join(_take_while_eq(first, second))


def _take_while_eq(first, second):
    """Iterate over two iterables while their values are equal."""
    for x, y in zip(first, second):
        if x == y:
            yield x
        else:
            return


_INDENT_PATTERN = re.compile(r'^\s*')


def _find_indent(string):
    """Find the indent of the string."""
    return _INDENT_PATTERN.search(string).group(0)


class _CommonIndentFinder(_CommonPrefixFinder):

    """Find the common prefix of any number of strings.

    _CommonPrefixFinder behaves mostly like the superclass, except only strings
    are allowed, and the common prefix is automatically trimmed down to leading
    whitespace (indentation).
    """

    def _set_prefix(self, value):
        super()._set_prefix(_find_indent(value))
