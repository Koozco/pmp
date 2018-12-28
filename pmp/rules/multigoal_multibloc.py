from pmp.rules.tbloc import TBloc
from .._common import solve_methods_registry

from .threshold_rule import ThresholdRule
from .multigoal_rule import MultigoalRule

algorithm = solve_methods_registry()


class MultigoalTBloc(MultigoalRule):
    """Multi-Bloc Voting Rule."""

    methods = algorithm.registry

    def __init__(self, thresholds, weights=None):
        MultigoalRule.__init__(self,
                               [ThresholdRule(TBloc(i + 1), t) for i, t in enumerate(thresholds)])
        self.weights = weights

    def find_committees(self, k, profile, method=None):
        if method is None:
            committee = algorithm.registry.default(self, k, profile)
        else:
            committee = algorithm.registry.all[method](self, k, profile)
        return committee

    @algorithm('Bruteforce', 'Exponential.')
    def _brute_tbloc(self, k, profile):
        return self._brute(k, profile)

    @algorithm('ILP', default=True)
    def _ilp_tbloc(self, k, profile):
        return self._ilp_weakly_separable(k, profile)
