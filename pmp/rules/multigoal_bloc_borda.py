from .._common import solve_methods_registry

from .threshold_rule import ThresholdRule
from .multigoal_rule import MultigoalRule
from .borda import Borda
from .bloc import Bloc

algorithm = solve_methods_registry()


class MultigoalBlocBorda(MultigoalRule):
    methods = algorithm.registry

    def __init__(self, (s1, s2)=(0, 0), weights=None, log_errors=True):
        MultigoalRule.__init__(self,
                               [ThresholdRule(Bloc(), s1),
                                ThresholdRule(Borda(), s2)],
                               log_errors=log_errors)
        self.weights = weights

    def find_committees(self, k, profile, method=None):
        if method is None:
            committee = algorithm.registry.default(self, k, profile)
        else:
            committee = algorithm.registry.all[method](self, k, profile)
        return committee

    @algorithm('Bruteforce', 'Exponential.')
    def _brute_bloc_borda(self, k, profile):
        return self._brute(k, profile)

    @algorithm('ILP', default=True)
    def _ilp(self, k, profile):
        return self._ilp_weakly_separable(k, profile)
