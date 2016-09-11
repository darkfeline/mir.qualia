import pytest

from mir.qualia import qualifier


@pytest.mark.parametrize(
    'comment_prefix,lines,is_commented', [
        ('#', ['foo', 'bar'], False),
        ('#', ['foo', '#bar'], False),
        ('#', ['#foo', '#bar'], True),
        ('#', ['#foo', '# bar'], True),
    ])
def test_is_commented(comment_prefix, lines, is_commented):
    prefix = qualifier.CommentPrefix(comment_prefix)
    assert prefix.is_commented(lines) is is_commented
