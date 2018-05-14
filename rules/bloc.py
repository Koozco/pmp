from .weakly_separable import WeaklySeparable


class Bloc(WeaklySeparable):
    """Bloc vote scoring rule."""

    def __init__(self, committee_size, candidates):
        WeaklySeparable.__init__(self, committee_size, candidates)
        self.weights = self.__bloc_weights(len(candidates), committee_size)
        self.scores = {}

    @staticmethod
    def __bloc_weights(size, k):
        weights = [1] * k + [0] * (size - k)
        return weights

    def compute_score(self, candidate, preferences):
        score = 0
        for pref in preferences:
            score += 1 if pref.order[0] == candidate else 0
        return score

    def compute_candidate_scores(self, preferences):
        self.scores = self._clean_scores()
        for pref in preferences:
            for i in range(0, self.k):
                self.scores[pref.order[i]] += self.weights[i]

    def copy_rule(self, candidates):
        return Bloc(self.k, candidates)
