from itertools import combinations

from .tie_breaking import random_winner


class MultigoalRule:
    """Scoring rule."""

    def __init__(self, rule1, rule2, tie_break=random_winner):
        self.rule1 = rule1
        self.rule2 = rule2
        self.tie_break = tie_break
        self.scores = {}

    def find_committees(self, k, profile, method=None):
        raise NotImplementedError()

    def compute_scores(self, k, profile):
        self.scores = {}
        all = list(combinations(profile.candidates, k))
        for comm in all:
            self.scores[comm] = self.committee_score(comm, profile)
        return self.scores

    def committee_score(self, committee, profile):
        score1 = self.rule1.rule.committee_score(committee, profile)
        score2 = self.rule2.rule.committee_score(committee, profile)
        return score1, score2
