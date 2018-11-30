from operator import itemgetter
from six import iteritems
from itertools import combinations

from .._common import solve_methods_registry
from .rule import Rule

algorithm = solve_methods_registry()


class PAV(Rule):
    """Proportional Approval Voting scoring rule."""

    methods = algorithm.registry

    def __init__(self, alpha=None):
        Rule.__init__(self)
        self.scores = {}
        self.alpha = alpha if alpha is not None else self._harmonic_alpha

    def find_committee(self, k, profile, method=None):
        self.scores = {}
        if method is None:
            method = algorithm.registry.default
        committee = algorithm.registry.all[method](self, k, profile)
        return committee

    @algorithm('Bruteforce', 'Exponential.', default=True)
    def brute(self, k, profile):
        self.scores = self.compute_scores(k, profile)
        return max(iteritems(self.scores), key=itemgetter(1))[0]

    def compute_scores(self, k, profile):
        scores = {}
        all = list(combinations(profile.candidates, k))
        for comm in all:
            scores[comm] = self.committee_score(set(comm), profile)
        return scores

    def committee_score(self, committee, profile):
        score = 0
        for pref in profile.preferences:
            satisfaction = self.satisfaction(len(committee & pref.approved))
            score += satisfaction
        return score

    def satisfaction(self, k):
        return sum([self.alpha(i + 1) for i in range(k)])

    @staticmethod
    def _harmonic_alpha(i):
        return 1.0 / i
