import pytest

from expects import *
from pmp.preferences import Ordinal


def test_compare_candidates(ordinal):
    a = 4
    b = 2
    better = ordinal.compare_candidates(a, b)
    expect(better).to(equal(a))


def test_worse_candidates_count(ordinal):
    candidate = 4
    expected_worse = 3
    worse = ordinal.worse_candidates_count(candidate)
    expect(worse).to(equal(expected_worse))


def test_better_candidates_count(ordinal):
    candidate = 4
    expected_better = 1
    better = ordinal.better_candidates_count(candidate)
    expect(better).to(equal(expected_better))


def test_is_valid_with_valid_preference(ordinal):
    expect(ordinal.is_valid(5)).to(be_true)


@pytest.mark.parametrize("pref_size", [4, 6])
def test_is_valid_with_invalid_preference_size(ordinal, pref_size):
    expect(ordinal.is_valid(pref_size)).to(be_false)


def test_is_valid_with_invalid_candidates():
    order = [5, 4, 3, 4, 1]
    ordinal = Ordinal(order)
    expect(ordinal.is_valid(5)).to(be_false)
