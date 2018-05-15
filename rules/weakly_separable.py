from .rule import Rule


class WeaklySeparable(Rule):
    """ Weakly Separable scoring rule """

    def __init__(self, k):
        Rule.__init__(self)
        self.k = k
        self.weights = []
        self.scores = {}

    def _clean_scores(self, candidates):
        self.scores = {candidate: 0 for candidate in candidates}

    # function to arbitrate ties
    def get_committee(self, winners):
        return [w for w in winners[:self.k]]

    def find_committee(self, profile, k, candidates, preferences):
        self._clean_scores(candidates)
        self.compute_candidate_scores(candidates, preferences)
        winners = sorted(self.scores, key=lambda x: self.scores[x], reverse=True)
        committee = self.get_committee(winners)
        return committee
