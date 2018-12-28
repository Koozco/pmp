from .weakly_separable import WeaklySeparable


class TBloc(WeaklySeparable):
    """Bloc vote scoring rule."""
    def __init__(self, t):
        WeaklySeparable.__init__(self)
        self.t = t

    def initialise_weights(self, _k, _profile):
        self.weights = [1] * self.t

    def find_committee(self, k, profile):
        self.initialise_weights(k, profile)
        committee = WeaklySeparable.find_committee(self, k, profile)
        return committee

    def compute_score(self, candidate, k, profile):
        self.initialise_weights(k, profile)
        score = WeaklySeparable.compute_score(self, candidate, k, profile)
        return score
