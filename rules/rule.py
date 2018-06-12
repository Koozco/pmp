from .tie_breaking import random_winner


class Rule:
    """Scoring rule."""

    def __init__(self, tie_break=random_winner):
        self.tie_break = tie_break

    def find_committee(self, k, profile):
        raise NotImplementedError()

    def compute_candidate_scores(self, k, profile):
        """Fill self.scores hash"""
        raise NotImplementedError()

    def compute_committee_score(self, committee, k, profile):
        raise NotImplementedError()
