from itertools import combinations
from operator import itemgetter

from .rule import Rule


class ChamberlinCourant(Rule):
    """Chamberlin-Courant vote scoring rule."""

    def __init__(self, committee_size, candidates, preferences, weights=None):
        Rule.__init__(self, committee_size, candidates, preferences)
        self.weights = weights if weights is not None else self.__borda_weights(len(candidates))
        self.scores = {}

    @staticmethod
    def __borda_weights(size):
        weights = [size - i for i in range(1, size + 1)]
        return weights

    def satisfaction(self, pref, cand):
        i = pref.order.index(cand)
        return self.weights[i]

    def committee_score(self, committee):
        score = 0
        for pref in self.preferences:
            satisfaction = [self.satisfaction(pref, cand) for cand in committee]
            score += max(satisfaction)
        return score

    def compute_scores(self):
        all = list(combinations(self.candidates, self.k))
        for comm in all:
            self.scores[comm] = self.committee_score(comm)

    def get_winner(self):
        return max(self.scores.iteritems(), key=itemgetter(1))
