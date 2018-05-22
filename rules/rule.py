class Rule:
    """Scoring rule."""

    def find_committee(self, profile):
        raise NotImplementedError()

    def compute_candidate_scores(self, profile):
        """Fill self.scores hash"""
        raise NotImplementedError()

    def compute_score(self, candidate, profile):
        raise NotImplementedError()
