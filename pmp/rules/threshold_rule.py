from .tie_breaking import random_winner


class ThresholdRule:
    """Scoring rule."""

    def __init__(self, rule, s, tie_break=random_winner):
        self.rule = rule
        self.s = s
        self.tie_break = tie_break

    def verify_committee_score(self, committee, profile):
        score = self.rule.committee_score(committee, profile)
        return score >= self.s
