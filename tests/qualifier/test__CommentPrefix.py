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
        # Uncommenting is idempotent.
        ('#', ['foo', 'bar'], ['foo', 'bar']),
        # Uncommenting only works if all lines are commented.
        ('#', ['foo', '#bar'], ['foo', '#bar']),
        # Regular uncommenting.
        ('#', ['#foo', '#bar'], ['foo', 'bar']),
        # Uncomment multiple times to be idempotent.
        ('#', ['##foo', '###bar'], ['foo', '#bar']),
        # Preserve indentation before prefix.
        ('#', [' #foo', ' #bar'], [' foo', ' bar']),
        # Preserve indentation after prefix.
        ('#', ['#foo', '# bar'], ['foo', ' bar']),
    ])
def test_uncomment(comment_prefix, lines, expected_lines):
    prefix = qualifier._CommentPrefix(comment_prefix)
    assert prefix.uncomment(lines) == expected_lines


@pytest.mark.parametrize(
    'comment_prefix,lines,expected_lines', [
        # Commenting.
        ('#', ['foo', 'bar'], ['#foo', '#bar']),
        # Commenting is idempotent.
        ('#', ['#foo', '#bar'], ['#foo', '#bar']),
        # Commenting preserves indentation.
        ('#', ['foo', ' bar'], ['#foo', '# bar']),
        # Commenting "moves past" common indentation.
        ('#', [' foo', '  bar'], [' #foo', ' # bar']),
    ])
def test_comment(comment_prefix, lines, expected_lines):
    prefix = qualifier._CommentPrefix(comment_prefix)
    assert prefix.comment(lines) == expected_lines
