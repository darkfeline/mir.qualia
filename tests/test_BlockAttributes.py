from mir.qualia import qualifier


def test_BlockAttributes_repr():
    attrs = qualifier._BlockAttributes(
        prefix='#',
        quality='firis',
    )
    assert repr(attrs) == "_BlockAttributes(prefix='#', quality='firis')"
