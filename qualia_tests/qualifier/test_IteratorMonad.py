import pytest
from qualia.qualifier import IteratorMonad


@pytest.mark.parametrize(
    'monad,expected',
    [
        (IteratorMonad(), []),
        (IteratorMonad(['foo']), ['foo']),
        (IteratorMonad(['foo'])
         .bind(['bar']), ['foo', 'bar']),
        (IteratorMonad(['foo'])
         .bind(['bar'])
         .bind(x for x in range(3)), ['foo', 'bar', 0, 1, 2]),
    ]
)
def test_IteratorMonad(monad, expected):
    assert list(monad) == expected
