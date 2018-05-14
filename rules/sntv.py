from .weakly_separable import WeaklySeparable


class SNTV(WeaklySeparable):
    """Single non-transferable vote scoring rule."""

    def __init__(self, committee_size, candidates):
        WeaklySeparable.__init__(self, committee_size, candidates)
        self.weights = self.__sntv_weights(len(candidates))
        self.scores = self.__clean_scores()

    @staticmethod
    def __sntv_weights(size):
        weights = [0] * size
        weights[0] = 1
        return weights

    def __clean_scores(self):
        return {candidate: 0 for candidate in self.candidates}

    def compute_score(self, candidate, preferences):
        score = 0
        for pref in preferences:
            score += 1 if pref.order[0] == candidate else 0
        return score

    def compute_candidate_scores(self, preferences):
        self.scores = self.__clean_scores()
        for pref in preferences:
            pref_winner = pref.order[0]
            self.scores[pref_winner] += 1

    def copy_rule(self):
        return SNTV(self.k, self.candidates)
