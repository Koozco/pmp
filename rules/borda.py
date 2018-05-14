from .weakly_separable import WeaklySeparable


class Borda(WeaklySeparable):
    """Borda vote scoring rule."""

    def __init__(self, committee_size, candidates):
        WeaklySeparable.__init__(self, committee_size, candidates)
        self.weights = self.__borda_weights(committee_size)

    @staticmethod
    def __borda_weights(size):
        weights = [size - i for i in range(1, size + 1)]
        return weights

    def compute_score(self, candidate, preferences):
        score = 0
        for pref in preferences:
            candidate_id = pref.order.index(candidate)
            score += pref.weights[candidate_id]
        return score

    def compute_candidate_scores(self, preferences):
        self.scores = self._clean_scores()
        for pref in preferences:
            for i in range(0, len(self.candidates)):
                self.scores[pref.order[i]] += self.weights[i]

    def copy_rule(self, candidates):
        return Borda(self.k, candidates)
