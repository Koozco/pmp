class Rule:
    """Scoring rule."""

    def __init__(self):
        self.algorithm = None

    def find_committee(self, profile, k, preferences):
        raise NotImplementedError()

    def compute_candidate_scores(self, preferences):
        """Fill self.scores hash"""
        raise NotImplementedError()

    def compute_score(self, candidate, preferences):
        raise NotImplementedError()

    def copy_rule(self, candidates):
        """Create identical scoring rule."""
        raise NotImplementedError()
