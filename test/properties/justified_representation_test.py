import pytest
from expects import *
from pmp.preferences import Profile, Approval
from pmp.properties import justified_representation


@pytest.fixture
def profile():
    """
    |V| = 9
    |C| = 5
    k = 3
    Easiest way to visualize this election is to draw this graphically on a grid
    Place voters on 3x3 square, [ [v1, v2, v3], [v4, v5, v6], [v7, v8, v9] ]
    Then mark candidates as shapes containing voters who support them
    """
    voters = [
        [3, 4, 6],
        [4, 5, 6],
        [1, 4],
        [1, 2, 3],
        [1, 2],
        [1, 2],
        [1, 2, 3],
        [1, 2],
        [1, 2]
    ]
    candidates = [1, 2, 3, 4, 5, 6]
    preferences = [Approval(v) for v in voters]

    return Profile(candidates, preferences)


def test_justified_representation(profile):
    satysfying_winners = {2, 3, 5}
    unsatysfying_winners = {4, 5, 6}

    expect(justified_representation(profile, satysfying_winners)).to(be_true)
    expect(justified_representation(profile, unsatysfying_winners)).to(be_false)
