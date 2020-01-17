from .preference import Preference


class Ordinal(Preference):
    """Ordinal preference profile."""

    def __init__(self, order, weights=None):
        self.order = list(order)
        self.weights = weights
        self.candidates_num = len(self.order)

    def compare_candidates(self, candidate_a, candidate_b):
        """Returns the better one."""
        position_a = self.order.index(candidate_a)
        position_b = self.order.index(candidate_b)
        return candidate_a if position_a < position_b else candidate_b

    def worse_candidates_count(self, candidate):
        """Candidate's rank - from how many candidates the candidate is better."""
        return (self.candidates_num - 1) - self.order.index(candidate)

    def better_candidates_count(self, candidate):
        """Candidate's rank - from how many candidates the candidate is worse."""
        return self.order.index(candidate)

    def is_valid(self, num_cand):
        return len(self.order) == num_cand and len(set(self.order)) == num_cand
