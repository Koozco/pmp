import numpy as np
from itertools import combinations
from .._common import solve_methods_registry

from .tie_breaking import random_winner
from ..utils.ilp import *

algorithm = solve_methods_registry()


class MultigoalRule:
    def __init__(self, rules, tie_break=random_winner):
        self.rules = rules
        self.tie_break = tie_break
        self.scores = {}

    def find_committees(self, k, profile, method=None):
        if method is None:
            committee = algorithm.registry.default(self, k, profile)
        else:
            committee = algorithm.registry.all[method](self, k, profile)
        return committee

    def compute_scores(self, k, profile):
        self.scores = {}
        all = list(combinations(profile.candidates, k))
        for comm in all:
            self.scores[comm] = self.committee_score(comm, profile)
        return self.scores

    def committee_score(self, committee, profile):
        return [rule.rule.committee_score(committee, profile) for rule in self.rules]

    def _brute(self, k, profile):
        self.compute_scores(k, profile)
        res = []
        for comm in self.scores:
            if self.scores[comm] >= [rule.s for rule in self.rules]:
                res.append(comm)

        return res

    def _ilp_weakly_separable(self, k, profile):
        # ILP
        m = len(profile.candidates)

        model = Model()

        # Xi - ith candidate is in committee
        x = ['x{}'.format(i) for i in range(m)]
        x_lb = np.zeros(m)
        x_ub = np.ones(m)
        model.add_variables(x, x_lb, x_ub)

        # Constraint1 - Vi Ei xi = k
        # K candidates are chosen
        xi = np.ones(m)
        model.add_constraint(x, xi, Sense.eq, k)

        # Constraint2 - thresholds
        for rule in self.rules:
            profile.scores = {}
            rule.rule.initialise_weights(profile)
            rule.rule.compute_candidate_scores(k, profile)
            model.add_constraint(x, [profile.scores[i] for i in range(m)], Sense.gt, rule.s)

        # End of definition

        model.solve()

        solution = model.get_solution()
        committee = (i for i in range(m) if solution['x{}'.format(i)] == 1)

        return committee
