from mir.qualia.comment import CommentPrefix


def test_is_commented_empty():
    prefix = CommentPrefix('#')
    assert prefix.is_commented([])


def test_is_commented_neither():
    prefix = CommentPrefix('#')
    assert not prefix.is_commented(['foo', 'bar'])


def test_is_commented_one():
    prefix = CommentPrefix('#')
    assert not prefix.is_commented(['foo', '#bar'])


def test_is_commented_both():
    prefix = CommentPrefix('#')
    assert prefix.is_commented(['#foo', '#bar'])


def test_is_commented_leading_whitespace():
    prefix = CommentPrefix('#')
    assert prefix.is_commented(['#foo', '  #bar'])


def test_uncomment_empty():
    prefix = CommentPrefix('#')
    got = prefix.uncomment([])
    assert got == []


def test_uncomment_idempotent():
    prefix = CommentPrefix('#')
    got = prefix.uncomment(['foo', 'bar'])
    assert got == ['foo', 'bar']


def test_uncomment_preserve_partial():
    prefix = CommentPrefix('#')
    got = prefix.uncomment(['foo', '#bar'])
    assert got == ['foo', '#bar']


def test_uncomment():
    prefix = CommentPrefix('#')
    got = prefix.uncomment(['#foo', '#bar'])
    assert got == ['foo', 'bar']


def test_uncomment_many_levels():
    prefix = CommentPrefix('#')
    got = prefix.uncomment(['##foo', '###bar'])
    assert got == ['foo', '#bar']


def test_uncomment_indentation_before():
    prefix = CommentPrefix('#')
    got = prefix.uncomment([' #foo', '  #bar'])
    assert got == [' foo', '  bar']


def test_uncomment_indentation_after():
    prefix = CommentPrefix('#')
    got = prefix.uncomment(['#foo', '# bar'])
    assert got == ['foo', ' bar']


def test_uncomment_indentation_before_after():
    prefix = CommentPrefix('#')
    got = prefix.uncomment(['#foo', ' # bar'])
    assert got == ['foo', '  bar']


def test_comment():
    prefix = CommentPrefix('#')
    got = prefix.comment(['foo', 'bar'])
    assert got == ['#foo', '#bar']


def test_comment_idempotent():
    prefix = CommentPrefix('#')
    got = prefix.comment(['#foo', '#bar'])
    assert got == ['#foo', '#bar']


def test_comment_preserve_indent():
    prefix = CommentPrefix('#')
    got = prefix.comment(['foo', ' bar'])
    assert got == ['#foo', '# bar']


def test_comment_skip_common_indent():
    prefix = CommentPrefix('#')
    got = prefix.comment([' foo', '  bar'])
    assert got == [' #foo', ' # bar']


def test_CommentPrefix_repr():
    finder = CommentPrefix('#')
    assert repr(finder) == "CommentPrefix('#')"
