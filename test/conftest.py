import pytest

from pmp.preferences import Ordinal, Approval
from pmp.experiments import Experiment


@pytest.fixture
def experiment():
    experiment = Experiment()
    return experiment


@pytest.fixture
def ordinal():
    order = [5, 4, 3, 2, 1]
    weights = [1, 2, 3, 4, 5]
    return Ordinal(order, weights)


@pytest.fixture
def approval():
    approved = set([1, 2, 3, 4, 5])
    return Approval(approved)


@pytest.fixture
def approval_factory():
    def _approval(size):
        approved = set([i + 1 for i in range(size)])
        return Approval(approved)

    return _approval


@pytest.fixture
def ordinal_factory():
    def _ordinal(size):
        order = [i + 1 for i in range(size)]
        weights = [i + 1 for i in range(size)]
        return Ordinal(order, weights)

    return _ordinal
