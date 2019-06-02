from operator import itemgetter
from six import iteritems
from itertools import combinations, product, chain
import numpy as np

from .._common import solve_methods_registry
from ..utils.ilp import Model, Sense, Objective, VariableTypes
from .rule import Rule

algorithm = solve_methods_registry()


class PAV(Rule):
    """Proportional Approval Voting scoring rule."""

    methods = algorithm.registry

    def __init__(self, alpha=None):
        """Alpha should be a function accepting int argument i"""
        Rule.__init__(self)
        self.scores = {}
        self.alpha = alpha if alpha is not None else self._harmonic_alpha

    def find_committee(self, k, profile, method=None):
        self.scores = {}
        if method is None:
            method = algorithm.registry.default
        committee = algorithm.registry.all[method](self, k, profile)
        return committee

    @algorithm('Bruteforce', 'Exponential.')
    def _brute(self, k, profile):
        self.scores = self._compute_scores(k, profile)
        return max(iteritems(self.scores), key=itemgetter(1))[0]

    @algorithm('ILP', default=True)
    def _ilp(self, k, profile):
        """ILP formulation from paper:
        https://arxiv.org/abs/1609.03537"""
        m = len(profile.candidates)
        n = len(profile.preferences)
        all_il = np.fromiter(chain.from_iterable(product(range(n), range(k))), int, n * k * 2)
        all_il.shape = n * k, 2

        model = Model()

        # yi - ith candidate is in committee
        y = ['y{}'.format(i) for i in range(m)]
        y_lb = np.zeros(m)
        y_ub = np.ones(m)
        model.add_variables(y, y_lb, y_ub)

        # xil - ith voter gets satisfaction for lth candidate he approves
        x = ['x{}_{}'.format(i, l) for (i, l) in all_il]
        x_lb = np.zeros(n * k)
        x_ub = np.ones(n * k)
        model.add_variables(x, x_lb, x_ub)

        # Objective - alpha_l * x_i_l
        model.set_objective_sense(Objective.maximize)
        objective_weights = [self.alpha(l + 1) for (_, l) in all_il]
        model.set_objective(x, objective_weights)

        # Constraint1 - Vi Ei xi = k
        # K candidates are chosen
        yi = np.ones(m)
        model.add_constraint(y, yi, Sense.eq, k)

        # Constraint2 - Vi El xil <= E(i approves c) yc
        # <=> Vi El xil - E(i approves c) yc <= 0
        c2_variables = [
            ['x{}_{}'.format(i, l) for l in range(k)] +
            ['y{}'.format(profile.candidates.index(c)) for c in profile.preferences[i].approved]
            for i in range(n)
        ]
        # coefficients for x's
        ones = np.ones((n, k))
        # coefficients for y's
        minus_ones = np.full((n, k), -1)
        c2_coefficients = np.concatenate((ones, minus_ones), axis=1)
        c2_senses = np.full(n, Sense.lt)
        c2_rights = np.zeros(n)
        model.add_constraints(c2_variables, c2_coefficients, c2_senses, c2_rights)

        # End of definition

        model.solve()

        solution = model.get_solution()
        committee = (profile.candidates[i] for i in range(m) if solution['y{}'.format(i)] == 1)

        self.scores[committee] = model.get_objective_value()
        return committee

    def _compute_scores(self, k, profile):
        scores = {}
        all = list(combinations(profile.candidates, k))
        for comm in all:
            scores[comm] = self._committee_score(set(comm), profile)
        return scores

    def _committee_score(self, committee, profile):
        score = 0
        for pref in profile.preferences:
            satisfaction = self._satisfaction(len(committee & pref.approved))
            score += satisfaction
        return score

    def _satisfaction(self, k):
        return sum([self.alpha(i + 1) for i in range(k)])

    @staticmethod
    def _harmonic_alpha(i):
        return 1.0 / i
