import pytest

from qualia import qualifier


@pytest.mark.parametrize(
    'comment_prefix,lines,active', [
        ('#', ['foo', 'bar'], True),
        ('#', ['foo', '#bar'], True),
        ('#', ['#foo', '#bar'], False),
        ('#', ['#foo', '# bar'], False),
    ])
def test_active(comment_prefix, lines, active):
    block = qualifier.QualifiedBlock(comment_prefix, lines)
    assert block.active is active


@pytest.mark.parametrize(
    'comment_prefix,lines,expected_lines', [
        ('#', ['foo', 'bar'], ['foo', 'bar']),
        ('#', ['foo', '#bar'], ['foo', '#bar']),
        ('#', ['#foo', '#bar'], ['foo', 'bar']),
        ('#', ['#foo', '# bar'], ['foo', 'bar']),
        ('#', ['## foo', '# bar'], ['# foo', 'bar']),
    ])
def test_activate(comment_prefix, lines, expected_lines):
    block = qualifier.QualifiedBlock(comment_prefix, lines)
    block.activate()
    assert block.lines == expected_lines
