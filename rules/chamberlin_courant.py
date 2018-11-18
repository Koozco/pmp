from itertools import combinations
from operator import itemgetter

from .rule import Rule


class ChamberlinCourant(Rule):
    """Chamberlin-Courant vote scoring rule."""

    def __init__(self, weights=None):
        Rule.__init__(self)
        self.weights = weights
        self.scores = {}

    def find_committee(self, k, profile):
        if self.weights is None:
            self.weights = self._borda_weights(len(profile.candidates))
        self.scores = self.compute_scores(k, profile)
        return max(self.scores.iteritems(), key=itemgetter(1))[0]

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
