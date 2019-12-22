from .weakly_separable import WeaklySeparable


class Bloc(WeaklySeparable):
    """Bloc vote scoring rule"""

    def find_committee(self, k, profile):
        self.weights = self._bloc_weights(k)
        committee = WeaklySeparable.find_committee(self, k, profile)
        return committee

    def compute_score(self, candidate, k, profile):
        self.weights = self._bloc_weights(k)
        score = WeaklySeparable.compute_score(self, candidate, k, profile)
        return score

    def _bloc_weights(self, k):
        return [1] * k
