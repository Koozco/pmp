class Rule:
    """Scoring rule."""

    def __init__(self, committee_size, candidates, preferences):
        self.k = committee_size
        self.candidates = list(candidates)
        self.preferences = list(preferences)
        self.algorithm = None

    def find_committee(self):
        raise NotImplementedError()

    def compute_candidate_scores(self):
        """Fill self.scores hash"""
        raise NotImplementedError()

    def compute_score(self, candidate):
        raise NotImplementedError()

    def copy_rule(self):
        """Create identical scoring rule."""
        raise NotImplementedError()
