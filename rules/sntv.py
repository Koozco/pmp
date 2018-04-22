from .rule import Rule


class Sntv(Rule):
    """Single non-transferable vote scoring rule."""

    def __init__(self, committee_size, candidates, preferences):
        Rule.__init__(self, committee_size, candidates, preferences)
        self.weights = self.__sntv_weights(len(candidates))
        self.scores = self.__clean_scores()

    @staticmethod
    def __sntv_weights(size):
        weights = [0] * size
        weights[0] = 1
        return weights

    def __clean_scores(self):
        return {candidate: 0 for candidate in self.candidates}

    def compute_score(self, candidate):
        score = 0
        for pref in self.preferences:
            score += 1 if pref.order[0] == candidate else 0
        return score

    def compute_candidate_scores(self):
        self.scores = self.__clean_scores()
        for pref in self.preferences:
            pref_winner = pref.order[0]
            self.scores[pref_winner] += 1

    def find_committee(self):
        self.compute_candidate_scores()
        winners = sorted(self.scores, key=lambda x: self.scores[x], reverse=True)
        committee = [w for w in winners[:self.k]]
        return committee

    def copy_rule(self):
        return Sntv(self.k, self.candidates, self.preferences)
