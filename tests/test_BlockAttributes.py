from mir.qualia import qualifier


def test_BlockAttributes_repr():
    attrs = qualifier._BlockAttributes(
        prefix='#',
        quality='firis',
    )
    assert repr(attrs) == "_BlockAttributes(prefix='#', quality='firis')"


def test_is_active():
    attrs = qualifier._BlockAttributes(
        prefix='#',
        quality='firis',
    )
    assert attrs.is_active({'firis', 'sophie'})


def test_not_is_active():
    attrs = qualifier._BlockAttributes(
        prefix='#',
        quality='firis',
    )
    assert not attrs.is_active({'sophie'})
