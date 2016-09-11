import pytest

from mir.qualia import qualifier

_BASE_TEXT = """\
# BEGIN spam
#spam
# END spam

# BEGIN eggs
#eggs
# END eggs
""".splitlines(True)

_SPAM_TEXT = """\
# BEGIN spam
spam
# END spam

# BEGIN eggs
#eggs
# END eggs
""".splitlines(True)

_EGGS_TEXT = """\
# BEGIN spam
#spam
# END spam

# BEGIN eggs
eggs
# END eggs
""".splitlines(True)

_FULL_TEXT = """\
# BEGIN spam
spam
# END spam

# BEGIN eggs
eggs
# END eggs
""".splitlines(True)


@pytest.mark.parametrize(
    'qualities,lines,expected', [
        ([], _BASE_TEXT, _BASE_TEXT),
        (['spam'], _BASE_TEXT, _SPAM_TEXT),
        (['eggs'], _BASE_TEXT, _EGGS_TEXT),
        (['spam', 'eggs'], _BASE_TEXT, _FULL_TEXT),
    ])
def test_qualifier(qualities, lines, expected):
    qual = qualifier.Qualifier(qualities)
    assert list(qual(lines)) == expected
