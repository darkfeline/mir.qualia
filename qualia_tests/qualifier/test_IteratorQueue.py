from mir.qualia import qualifier


def test_iteration():
    queue = qualifier.IteratorQueue([1, 2, 3])
    assert list(queue) == [1, 2, 3]
    assert list(queue) == []


def test_reiteration():
    queue = qualifier.IteratorQueue()
    assert list(queue) == []
    queue.extend([1, 2, 3])
    assert list(queue) == [1, 2, 3]


def test_multiple_extend():
    queue = qualifier.IteratorQueue()
    queue.extend([1])
    queue.extend([2])
    assert list(queue) == [1, 2]
