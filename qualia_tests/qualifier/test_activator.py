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
    activator = qualifier.Activator(comment_prefix)
    assert activator.is_active(lines) is active


@pytest.mark.parametrize(
    'comment_prefix,lines,expected_lines', [
        ('#', ['foo', 'bar'], ['foo', 'bar']),
        ('#', ['foo', '#bar'], ['foo', '#bar']),
        ('#', ['#foo', '#bar'], ['foo', 'bar']),
        ('#', ['#foo', '# bar'], ['foo', 'bar']),
        ('#', ['## foo', '# bar'], ['# foo', 'bar']),
        ('#', ['## foo', '### bar'], ['foo', '# bar']),
    ])
def test_activate(comment_prefix, lines, expected_lines):
    activator = qualifier.Activator(comment_prefix)
    assert activator.activate(lines) == expected_lines


@pytest.mark.parametrize(
    'comment_prefix,lines,expected_lines', [
        ('#', ['foo', 'bar'], ['#foo', '#bar']),
        ('#', ['foo', '# bar'], ['#foo', '## bar']),
        ('#', ['#foo', '# bar'], ['#foo', '# bar']),
        ('#', ['#foo', '## bar'], ['#foo', '## bar']),
    ])
def test_deactivate(comment_prefix, lines, expected_lines):
    activator = qualifier.Activator(comment_prefix)
    assert activator.deactivate(lines) == expected_lines
