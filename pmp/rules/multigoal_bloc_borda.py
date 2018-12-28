import numpy as np
from ..utils.ilp import *
from .._common import solve_methods_registry

from .threshold_rule import ThresholdRule
from .multigoal_rule import MultigoalRule
from .borda import Borda
from .bloc import Bloc

algorithm = solve_methods_registry()


class MultigoalBlocBorda(MultigoalRule):
    methods = algorithm.registry

    def __init__(self, s1=0, s2=0, weights=None, log_errors=True):
        MultigoalRule.__init__(self,
                               ThresholdRule(Bloc(), s1),
                               ThresholdRule(Borda(), s2))
        self.weights = weights
        self.log_errors = log_errors

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
        # kBorda initialisation
        self.rule2.rule.initialise_weights(profile)
        self.rule2.rule.compute_candidate_scores(k, profile)

        # ILP
        m = len(profile.candidates)

        model = Model(log_errors=self.log_errors)

        # Xi - ith candidate is in committee
        x = ['x{}'.format(i) for i in range(m)]
        x_lb = np.zeros(m)
        x_ub = np.ones(m)
        model.add_variables(x, x_lb, x_ub)

        # Constraint1 - Vi Ei xi = k
        # K candidates are chosen
        xi = np.ones(m)
        model.add_constraint(x, xi, Sense.eq, k)

        # Constraint2 - Bloc
        bloc_candidate_scores = [self.rule1.rule.compute_score(i, k, profile) for i in range(m)]
        model.add_constraint(x, bloc_candidate_scores, Sense.gt, self.rule1.s)

        # Constraint3 - kBorda
        borda_candidate_scores = [profile.scores[i] for i in range(m)]
        model.add_constraint(x, borda_candidate_scores, Sense.gt, self.rule2.s)

        # End of definition

        model.solve()

        solution = model.get_solution()
        committee = (i for i in range(m) if abs(solution['x{}'.format(i)] - 1) <= 1e-05)

        return committee
