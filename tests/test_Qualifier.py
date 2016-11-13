import collections

import pytest

from mir.qualia import qualifier


def test_qualifier_repr():
    qual = qualifier.Qualifier(['sophie'])
    assert repr(qual) == "Qualifier(qualities=['sophie'])"


def test_qualifier():
    qual = qualifier.Qualifier([])
    got = list(qual([]))
    assert got == []


def test_qualifier_no_quality_idempotence():
    qual = qualifier.Qualifier([])
    got = list(qual([
        '# BEGIN spam\n',
        '#spam\n',
        '# END spam\n',
    ]))
    assert got == [
        '# BEGIN spam\n',
        '#spam\n',
        '# END spam\n',
    ]


def test_qualifier_with_quality_idempotence():
    qual = qualifier.Qualifier(['spam'])
    got = list(qual([
        '# BEGIN spam\n',
        'spam\n',
        '# END spam\n',
    ]))
    assert got == [
        '# BEGIN spam\n',
        'spam\n',
        '# END spam\n',
    ]


def test_qualifier_with_quality():
    qual = qualifier.Qualifier(['spam'])
    got = list(qual([
        '# BEGIN spam\n',
        '#spam\n',
        '# END spam\n',
    ]))
    assert got == [
        '# BEGIN spam\n',
        'spam\n',
        '# END spam\n',
    ]


def test_qualifier_no_quality():
    qual = qualifier.Qualifier([])
    got = list(qual([
        '# BEGIN spam\n',
        'spam\n',
        '# END spam\n',
    ]))
    assert got == [
        '# BEGIN spam\n',
        '#spam\n',
        '# END spam\n',
    ]


def test_qualifier_ignore_unclosed():
    qual = qualifier.Qualifier(['spam', 'eggs'])
    got = list(qual([
        '# BEGIN spam\n',
        '#spam\n',
        '# BEGIN eggs\n',
        '#eggs\n',
        '# END eggs\n',
    ]))
    assert got == [
        '# BEGIN spam\n',
        '#spam\n',
        '# BEGIN eggs\n',
        '#eggs\n',
        '# END eggs\n',
    ]


def test_qualifier_ignore_unqualified():
    qual = qualifier.Qualifier([])
    got = list(qual([
        'spam\n',
    ]))
    assert got == [
        'spam\n',
    ]


def test_qualifier_no_whitespace_before_keyword():
    qual = qualifier.Qualifier(['spam'])
    got = list(qual([
        '#BEGIN spam\n',
        '#spam\n',
        '#END spam\n',
    ]))
    assert got == [
        '#BEGIN spam\n',
        'spam\n',
        '#END spam\n',
    ]
