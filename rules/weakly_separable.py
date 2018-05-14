from .rule import Rule


class WeaklySeparable(Rule):
    """ Weakly Separable scoring rule """

    def __init__(self, k, candidates):
        Rule.__init__(self)
        self.candidates = candidates
        self.k = k
        self.weights = [0] * len(candidates)
        self.scores = self._clean_scores()

    def _clean_scores(self):
        return {candidate: 0 for candidate in self.candidates}

    # function to arbitrate ties
    def get_committee(self, winners):
        return [w for w in winners[:self.k]]

    def find_committee(self, profile, k, preferences):
        self.compute_candidate_scores(preferences=preferences)
        winners = sorted(self.scores, key=lambda x: self.scores[x], reverse=True)
        committee = self.get_committee(winners)
        return committee
