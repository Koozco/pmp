class Rule:
    """Scoring rule."""

    def find_committee(self, k, profile):
        raise NotImplementedError()

    def compute_candidate_scores(self, k, profile):
        """Fill self.scores hash"""
        raise NotImplementedError()

    def compute_committee_score(self, committee, k, profile):
        raise NotImplementedError()
