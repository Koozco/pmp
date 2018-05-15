from .weakly_separable import WeaklySeparable


class Borda(WeaklySeparable):
    """Borda vote scoring rule."""

    def __init__(self, committee_size):
        WeaklySeparable.__init__(self, committee_size)

    def __borda_weights(self, size):
        self.weights = [size - i for i in range(1, size + 1)]

    def compute_score(self, candidate, candidates, preferences):
        self.__borda_weights(len(candidates))
        score = 0
        for pref in preferences:
            candidate_id = pref.order.index(candidate)
            score += pref.weights[candidate_id]
        return score

    def compute_candidate_scores(self, candidates, preferences):
        self._clean_scores(candidates)
        self.__borda_weights(len(candidates))
        for pref in preferences:
            for i in range(0, len(candidates)):
                self.scores[pref.order[i]] += self.weights[i]

    def copy_rule(self):
        return Borda(self.k)
