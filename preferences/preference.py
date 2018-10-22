class Preference:
    """Single preference."""

    def __init__(self, order, weights=None):
        self.order = list(order)
        self.weights = weights
        self.candidates_num = len(self.order)

    def compare_candidates(self, candidate_a, candidate_b):
        """Compare candidates."""
        raise NotImplementedError()

    def worse_candidates_count(self, candidate):
        """Candidate's rank - from how many candidates the candidate is better."""
        raise NotImplementedError()

    def better_candidates_count(self, candidate):
        """Candidate's rank - from how many candidates the candidate is worse."""
        raise NotImplementedError()

    def is_valid(self, num_cand):
        raise NotImplementedError()
