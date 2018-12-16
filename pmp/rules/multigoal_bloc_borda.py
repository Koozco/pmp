from .._common import solve_methods_registry

from .threshold_rule import ThresholdRule
from .multigoal_rule import MultigoalRule
from .borda import Borda
from .bloc import Bloc

algorithm = solve_methods_registry()


class MultigoalBlocBorda(MultigoalRule):

    methods = algorithm.registry

    def __init__(self, s1=0, s2=0, weights=None):
        MultigoalRule.__init__(self,
                               ThresholdRule(Bloc(), s1),
                               ThresholdRule(Borda(), s2))
        self.weights = weights

    def find_committees(self, k, profile, method=None):
        if method is None:
            committee = algorithm.registry.default(self, k, profile)
        else:
            committee = algorithm.registry.all[method](self, k, profile)
        return committee

    @algorithm('Bruteforce', 'Exponential.')
    def _brute(self, k, profile):
        self.compute_scores(k, profile)
        res = []
        for comm in self.scores:
            if self.scores[comm] >= (self.rule1.s, self.rule2.s):
                res.append(comm)

        return res

    @algorithm('ILP', default=True)
    def _ilp(self, k, profile):
        """
        $x_i \in \{0, 1\}$ \ \ \ \ for i = 1, 2, ... m\\[4\jot]
        $\sum_{i=1}^{m} \ x_i = k$\\[4\jot]
        $\sum_{i=1}^{m} \ x_i \cdot \gamma_{m,k}^j(c_i) \geq s_j$ \ \ \ \ for j=1, 2, ... t
        """
        raise NotImplementedError()
