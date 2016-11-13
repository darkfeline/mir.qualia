import pytest

from mir.qualia import qualifier


def test_is_commented_empty():
    prefix = qualifier._CommentPrefix('#')
    assert prefix.is_commented([])


def test_is_commented_neither():
    prefix = qualifier._CommentPrefix('#')
    assert not prefix.is_commented(['foo', 'bar'])


def test_is_commented_one():
    prefix = qualifier._CommentPrefix('#')
    assert not prefix.is_commented(['foo', '#bar'])


def test_is_commented_both():
    prefix = qualifier._CommentPrefix('#')
    assert prefix.is_commented(['#foo', '#bar'])


def test_is_commented_leading_whitespace():
    prefix = qualifier._CommentPrefix('#')
    assert prefix.is_commented(['#foo', '  #bar'])


def test_uncomment_empty():
    prefix = qualifier._CommentPrefix('#')
    got = prefix.uncomment([])
    assert got == []


def test_uncomment_idempotent():
    prefix = qualifier._CommentPrefix('#')
    got = prefix.uncomment(['foo', 'bar'])
    assert got == ['foo', 'bar']


def test_uncomment_preserve_partial():
    prefix = qualifier._CommentPrefix('#')
    got = prefix.uncomment(['foo', '#bar'])
    assert got == ['foo', '#bar']


def test_uncomment():
    prefix = qualifier._CommentPrefix('#')
    got = prefix.uncomment(['#foo', '#bar'])
    assert got == ['foo', 'bar']


def test_uncomment_many_levels():
    prefix = qualifier._CommentPrefix('#')
    got = prefix.uncomment(['##foo', '###bar'])
    assert got == ['foo', '#bar']


def test_uncomment_indentation_before():
    prefix = qualifier._CommentPrefix('#')
    got = prefix.uncomment([' #foo', '  #bar'])
    assert got == [' foo', '  bar']


def test_uncomment_indentation_after():
    prefix = qualifier._CommentPrefix('#')
    got = prefix.uncomment(['#foo', '# bar'])
    assert got == ['foo', ' bar']


def test_uncomment_indentation_before_after():
    prefix = qualifier._CommentPrefix('#')
    got = prefix.uncomment(['#foo', ' # bar'])
    assert got == ['foo', '  bar']


def test_comment():
    prefix = qualifier._CommentPrefix('#')
    got = prefix.comment(['foo', 'bar'])
    assert got == ['#foo', '#bar']


def test_comment_idempotent():
    prefix = qualifier._CommentPrefix('#')
    got = prefix.comment(['#foo', '#bar'])
    assert got == ['#foo', '#bar']


def test_comment_preserve_indent():
    prefix = qualifier._CommentPrefix('#')
    got = prefix.comment(['foo', ' bar'])
    assert got == ['#foo', '# bar']


def test_comment_skip_common_indent():
    prefix = qualifier._CommentPrefix('#')
    got = prefix.comment([' foo', '  bar'])
    assert got == [' #foo', ' # bar']


def test_CommentPrefix_repr():
    finder = qualifier._CommentPrefix('#')
    assert repr(finder) == "_CommentPrefix('#')"
