from itertools import combinations, product, chain
from operator import itemgetter

import numpy as np
from six import iteritems

from .._common import solve_methods_registry

from ..utils.ilp import *
from .rule import Rule

algorithm = solve_methods_registry()


class ChamberlinCourant(Rule):
    """Chamberlin-Courant vote scoring rule."""

    methods = algorithm.registry

    def __init__(self, weights=None):
        Rule.__init__(self)
        self.weights = weights
        self.scores = {}

    def find_committee(self, k, profile, method=None):
        self.scores = {}
        if self.weights is None:
            self.weights = self._borda_weights(len(profile.candidates))

        if method is None:
            committee = algorithm.registry.default(self, k, profile)
        else:
            committee = algorithm.registry.all[method](self, k, profile)
        return committee

    @algorithm('Bruteforce', 'Exponential.')
    def _brute(self, k, profile):
        self.scores = self.compute_scores(k, profile)
        return max(iteritems(self.scores), key=itemgetter(1))[0]

    @algorithm('ILP', default=True)
    def _ilp(self, k, profile):
        m = len(profile.candidates)
        n = len(profile.preferences)
        all_ij = np.fromiter(chain.from_iterable(product(range(m), range(n))), int, n * m * 2)
        all_ij.shape = n * m, 2

        model = Model()

        # Xi - ith candidate is in committee
        x = ['x{}'.format(i) for i in range(m)]
        x_lb = np.zeros(m)
        x_ub = np.ones(m)
        model.add_variables(x, x_lb, x_ub)

        # Yij - ith candidate represents jth voter
        y = ['y{}_{}'.format(i, j) for (i, j) in all_ij]
        y_lb = np.zeros(n * m)
        y_ub = np.ones(n * m)
        model.add_variables(y, y_lb, y_ub)

        # Objective - alpha_j(i) * yij
        model.set_objective_sense(Objective.maximize)

        objective_iterable = (self.satisfaction(profile.preferences[j], profile.candidates[i]) for (i, j) in all_ij)
        yij_weights = np.fromiter(objective_iterable, int, n * m)
        model.set_objective(y, yij_weights)

        # Constraint1 - Vi Ei xi = k
        # K candidates are chosen
        xi = np.ones(m)
        model.add_constraint(x, xi, Sense.eq, k)

        # Constraint2 - Vi Ej yij = 1
        # Each voter is represented by one candidate
        c2_variables = [['y{}_{}'.format(i, j) for i in range(m)] for j in range(n)]
        c2_coefficients = np.ones((n, m))
        c2_senses = np.full(n, Sense.eq)
        c2_rights = np.ones(n)
        model.add_constraints(c2_variables, c2_coefficients, c2_senses, c2_rights)

        # Constraint3 - Vji yij <= xi
        # Candidate represent voter only if is chosen
        c3_variables = [['y{}_{}'.format(i, j), 'x{}'.format(i)] for (i, j) in all_ij]
        c3_coefficients = np.tile(np.array((1, -1)), n * m)
        c3_coefficients.shape = n * m, 2
        c3_senses = np.full(n * m, Sense.lt)
        c3_rights = np.zeros(n * m)
        model.add_constraints(c3_variables, c3_coefficients, c3_senses, c3_rights)

        # End of definition

        model.solve()

        solution = model.get_solution()
        committee = (i for i in range(m) if solution['x{}'.format(i)] == 1)

        self.scores[committee] = model.get_objective_value()
        return committee

    def compute_scores(self, k, profile):
        scores = {}
        all = list(combinations(profile.candidates, k))
        for comm in all:
            scores[comm] = self.committee_score(comm, profile)
        return scores

    def committee_score(self, committee, profile):
        score = 0
        for pref in profile.preferences:
            satisfaction = [self.satisfaction(pref, cand) for cand in committee]
            score += max(satisfaction)
        return score

    def satisfaction(self, pref, cand):
        i = pref.order.index(cand)
        return self.weights[i]

    @staticmethod
    def _borda_weights(size):
        weights = [size - i for i in range(1, size + 1)]
        return weights
