import mir.qualia.indent as indentlib


def test_take_while_eq_both_empty():
    got = list(indentlib._take_while_eq([], []))
    assert got == []


def test_take_while_eq_one_empty():
    got = list(indentlib._take_while_eq([], [1]))
    assert got == []


def test_take_while_eq_prefix_of_other():
    got = list(indentlib._take_while_eq([1, 2], [1, 2, 3]))
    assert got == [1, 2]


def test_take_while_eq_prefix_diverging():
    got = list(indentlib._take_while_eq([1, 2, 4], [1, 2, 3]))
    assert got == [1, 2]


def test_take_while_eq_prefix_same():
    got = list(indentlib._take_while_eq([1, 2, 3], [1, 2, 3]))
    assert got == [1, 2, 3]


def test_common_indent_empty():
    got = indentlib.common_indent([])
    assert got == ''


def test_common_indent_no_indent():
    got = indentlib.common_indent(['abc', 'abc'])
    assert got == ''


def test_common_indent():
    got = indentlib.common_indent([' abc', ' abc'])
    assert got == ' '


def test_common_indent_one_line_no_indent():
    got = indentlib.common_indent(['spam'])
    assert got == ''


def test_common_indent_one_line():
    got = indentlib.common_indent(['  spam'])
    assert got == '  '


def test_CommonPrefixFinder_repr():
    finder = indentlib._CommonPrefixFinder('firis')
    assert repr(finder) == "_CommonPrefixFinder('firis')"
