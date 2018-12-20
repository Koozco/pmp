from .tie_breaking import random_winner
from .._common import default_methods_registry


class Rule:
    """Scoring rule."""

    methods = default_methods_registry()

    def __init__(self, tie_break=random_winner):
        self.tie_break = tie_break

    def find_committee(self, k, profile):
        raise NotImplementedError()

    def compute_candidate_scores(self, k, profile):
        """Fill self.scores hash"""
        raise NotImplementedError()

    def compute_committee_score(self, committee, k, profile):
        raise NotImplementedError()
