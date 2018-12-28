from .weakly_separable import WeaklySeparable


class TBloc(WeaklySeparable):
    """Bloc vote scoring rule."""
    def __init__(self, t):
        WeaklySeparable.__init__(self)
        self.t = t

    def initialise_weights(self, _):
        self.weights = self._tbloc_weights()

    def find_committee(self, k, profile):
        self.initialise_weights(None)
        committee = WeaklySeparable.find_committee(self, k, profile)
        return committee

    def compute_score(self, candidate, k, profile):
        self.initialise_weights(None)
        score = WeaklySeparable.compute_score(self, candidate, k, profile)
        return score

    def _tbloc_weights(self):
        return [1] * self.t
