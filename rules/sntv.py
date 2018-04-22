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

    def find_committee(self):
        self.scores = self.__clean_scores()
        for pref in self.preferences:
            pref_winner = pref.order[0]
            self.scores[pref_winner] += 1

        winners = sorted(self.scores, key=lambda x: self.scores[x], reverse=True)
        committee = [w for w in winners[:self.k]]
        return committee
