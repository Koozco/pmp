from .weakly_separable import WeaklySeparable


class Bloc(WeaklySeparable):
    """Bloc vote scoring rule"""

    def find_committee(self, k, profile):
        if self.weights is None or len(self.weights) != k:
            self.weights = self._bloc_weights(k)
        committee = WeaklySeparable.find_committee(self, k, profile)
        return committee

    def compute_score(self, candidate, k, profile):
        if self.weights is None or len(self.weights) != k:
            self.weights = self._bloc_weights(k)
        score = WeaklySeparable.compute_score(self, candidate, k, profile)
        return score

    @staticmethod
    def _bloc_weights(k):
        return [1] * k
