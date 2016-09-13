import pytest

from mir.qualia import qualifier


def test_string():
    prefix = qualifier._CommentPrefix('#')
    assert str(prefix) == '#'


@pytest.mark.parametrize(
    'comment_prefix,lines,is_commented', [
        ('#', ['foo', 'bar'], False),
        ('#', ['foo', '#bar'], False),
        ('#', ['#foo', '#bar'], True),
        ('#', ['#foo', '# bar'], True),
    ])
def test_is_commented(comment_prefix, lines, is_commented):
    prefix = qualifier._CommentPrefix(comment_prefix)
    assert prefix.is_commented(lines) is is_commented


@pytest.mark.parametrize(
    'comment_prefix,lines,expected_lines', [
        ('#', ['foo', 'bar'], ['foo', 'bar']),
        ('#', ['foo', '#bar'], ['foo', '#bar']),
        ('#', ['#foo', '#bar'], ['foo', 'bar']),

        # Uncomment multiple times
        ('#', ['##foo', '###bar'], ['foo', '#bar']),

        # Comment with indentation
        (' #', [' #foo', '#bar'], [' #foo', '#bar']),
        (' #', [' #foo', ' #bar'], ['foo', 'bar']),

        # Preserving whitespace after comment
        ('#', ['#foo', '# bar'], ['foo', ' bar']),
    ])
def test_uncomment(comment_prefix, lines, expected_lines):
    prefix = qualifier._CommentPrefix(comment_prefix)
    assert prefix.uncomment(lines) == expected_lines


@pytest.mark.parametrize(
    'comment_prefix,lines,expected_lines', [
        ('#', ['foo', 'bar'], ['#foo', '#bar']),
        ('#', ['#foo', '#bar'], ['#foo', '#bar']),

        # Keep whitespace
        ('#', ['foo', ' bar'], ['#foo', '# bar']),
        (' #', ['foo', 'bar'], [' #foo', ' #bar']),
    ])
def test_comment(comment_prefix, lines, expected_lines):
    prefix = qualifier._CommentPrefix(comment_prefix)
    assert prefix.comment(lines) == expected_lines
