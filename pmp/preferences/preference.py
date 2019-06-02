class Preference:
    """Single preference."""

    def __init__(self, order=[], weights=None):
        self.order = list(order)
        self.weights = weights
        self.candidates_num = len(self.order)

    def is_valid(self, num_cand):
        raise NotImplementedError()
