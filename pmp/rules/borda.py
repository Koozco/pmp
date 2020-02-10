from .weakly_separable import WeaklySeparable


class Borda(WeaklySeparable):
    """Borda vote scoring rule"""

    def find_committee(self, k, profile):
        if self.weights is None or len(self.weights) != len(profile.candidates):
            self.weights = self._borda_weights(len(profile.candidates))
        committee = WeaklySeparable.find_committee(self, k, profile)
        return committee

    def compute_score(self, candidate, k, profile):
        if self.weights is None or len(self.weights) != len(profile.candidates):
            self.weights = self._borda_weights(len(profile.candidates))
        score = WeaklySeparable.compute_score(self, candidate, k, profile)
        return score

    @staticmethod
    def _borda_weights(size):
        return [size - i for i in range(1, size + 1)]
