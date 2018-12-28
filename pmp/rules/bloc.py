from .weakly_separable import WeaklySeparable


class Bloc(WeaklySeparable):
    """Bloc vote scoring rule."""

    def initialise_weights(self, k, _profile):
        self.weights = [1] * k

    def find_committee(self, k, profile):
        self.initialise_weights(k, profile)
        committee = WeaklySeparable.find_committee(self, k, profile)
        return committee

    def compute_score(self, candidate, k, profile):
        self.initialise_weights(k, profile)
        score = WeaklySeparable.compute_score(self, candidate, k, profile)
        return score
