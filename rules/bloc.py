from .weakly_separable import WeaklySeparable


class Bloc(WeaklySeparable):
    """Bloc vote scoring rule."""

    def __init__(self, committee_size, candidates, preferences):
        WeaklySeparable.__init__(self, committee_size, candidates, preferences)
        self.weights = self.__bloc_weights(len(candidates), committee_size)
        self.scores = {}

    @staticmethod
    def __bloc_weights(size, k):
        weights = [1] * k + [0] * (size - k)
        return weights

    def compute_score(self, candidate):
        score = 0
        for pref in self.preferences:
            score += 1 if pref.order[0] == candidate else 0
        return score

    def compute_candidate_scores(self):
        self.scores = self.__clean_scores()
        for pref in self.preferences:
            for i in range(0, self.k):
                self.scores[pref.order[i]] += self.weights[i]

    def copy_rule(self):
        return Bloc(self.k, self.candidates, self.preferences)
