class Rule:
    """Scoring rule."""

    def __init__(self):
        self.algorithm = None

    def find_committee(self, profile, k, candidates, preferences):
        raise NotImplementedError()

    def compute_candidate_scores(self, candidates, preferences):
        """Fill self.scores hash"""
        raise NotImplementedError()

    def compute_score(self, candidate, candidates, preferences):
        raise NotImplementedError()

    def copy_rule(self):
        """Create identical scoring rule."""
        raise NotImplementedError()
