import collections

import pytest

from mir.qualia import qualifier


_QUALIFIER_TEST_PARAMS = 'qualities,text,expected,msg'
_QualifierTest = collections.namedtuple('_QualifierTest',
                                        _QUALIFIER_TEST_PARAMS)


@pytest.mark.parametrize(
    _QUALIFIER_TEST_PARAMS, [
        _QualifierTest(
            qualities=[],
            text=(
                '# BEGIN spam\n'
                '#spam\n'
                '# END spam\n'),
            expected=(
                '# BEGIN spam\n'
                '#spam\n'
                '# END spam\n'),
            msg='inactive quality idempotence'),

        _QualifierTest(
            qualities=['spam'],
            text=(
                '# BEGIN spam\n'
                'spam\n'
                '# END spam\n'),
            expected=(
                '# BEGIN spam\n'
                'spam\n'
                '# END spam\n'),
            msg='active quality idempotence'),

        _QualifierTest(
            qualities=['spam'],
            text=(
                '# BEGIN spam\n'
                '#spam\n'
                '# END spam\n'),
            expected=(
                '# BEGIN spam\n'
                'spam\n'
                '# END spam\n'),
            msg='activating quality'),

        _QualifierTest(
            qualities=[],
            text=(
                '# BEGIN spam\n'
                'spam\n'
                '# END spam\n'),
            expected=(
                '# BEGIN spam\n'
                '#spam\n'
                '# END spam\n'),
            msg='deactivating quality'),

        _QualifierTest(
            qualities=['spam', 'eggs'],
            text=(
                '# BEGIN spam\n'
                '#spam\n'
                '# BEGIN eggs\n'
                '#eggs\n'
                '# END eggs\n'),
            expected=(
                '# BEGIN spam\n'
                '#spam\n'
                '# BEGIN eggs\n'
                '#eggs\n'
                '# END eggs\n'),
            msg='ignore unclosed blocks'),

        _QualifierTest(
            qualities=[],
            text=(
                'spam\n'),
            expected=(
                'spam\n'),
            msg='ignore unqualified line'),
    ])
def test_qualifier(qualities, text, expected, msg):
    lines = text.splitlines(keepends=True)
    expected_lines = expected.splitlines(keepends=True)
    qual = qualifier.Qualifier(qualities)
    assert list(qual(lines)) == expected_lines, msg
