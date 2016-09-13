import pytest

from mir.qualia import qualifier


@pytest.mark.parametrize(
    'line,expected', [
        ('', ''),
        ('spam', ''),
        ('  spam', '  '),
    ])
def test__get_indent(line, expected):
    assert qualifier._get_indent(line) == expected


@pytest.mark.parametrize(
    'lines,expected', [
        ([], ''),
        (['abc', 'def'], ''),
        ([' abc', ' def'], ' '),
    ])
def test__common_indent(lines, expected):
    assert qualifier._common_indent(lines) == expected
