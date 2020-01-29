import pytest

from expects import *
from pmp.preferences import Profile


@pytest.fixture
def profile(ordinal_factory):
    candidates = [1, 2, 3]
    preferences = [ordinal_factory(size=3) for _ in range(3)]
    return Profile(candidates, preferences)


def test_add_preference(profile, ordinal_factory):
    old_size = len(profile.preferences)
    pref = ordinal_factory(3)
    profile.add_preference(pref)
    new_size = len(profile.preferences)
    expect(new_size - old_size).to(equal(1))


def test_add_preference_with_invalid(profile, ordinal_factory):
    old_size = len(profile.preferences)
    pref = ordinal_factory(2)
    profile.add_preference(pref)
    new_size = len(profile.preferences)
    expect(new_size - old_size).to(equal(0))


def test_add_preferences(profile, ordinal_factory):
    old_size = len(profile.preferences)
    prefs = [ordinal_factory(3) for _ in range(3)]
    profile.add_preferences(prefs)
    new_size = len(profile.preferences)
    expect(new_size - old_size).to(equal(3))


def test_add_preferences_with_invalid(profile, ordinal_factory):
    old_size = len(profile.preferences)
    prefs = [ordinal_factory(3) for _ in range(2)] + [ordinal_factory(2)]
    profile.add_preferences(prefs)
    new_size = len(profile.preferences)
    print(new_size, old_size)
    expect(new_size - old_size).to(equal(0))
