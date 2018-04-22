from .preference import Preference


class Ordinal(Preference):
    """Ordinal preference profile."""

    def __init__(self, order, weights=None):
        Preference.__init__(self, order, weights)

    def compare_candidates(self, candidate_a, candidate_b):
        """Returns the better one."""
        position_a = self.order.index(candidate_a)
        position_b = self.order.index(candidate_b)
        return candidate_a if position_a < position_b else candidate_b

    def better(self, candidate):
        """Candidate's rank - from how many candidates the candidate is better."""
        return (self.candidates_num - 1) - self.order.index(candidate)

    def worse(self, candidate):
        """Candidate's rank - from how many candidates the candidate is worse."""
        return self.order.index(candidate)
