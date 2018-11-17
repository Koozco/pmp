from .weakly_separable import WeaklySeparable
from .tie_breaking import random_winner


class SNTV(WeaklySeparable):
    """Single non-transferable vote scoring rule."""

    def __init__(self, tie_break=random_winner):
        WeaklySeparable.__init__(self, [1], tie_break)

    def compute_score(self, candidate, k, profile):
        score = 0
        for pref in profile.preferences:
            score += 1 if pref.order[0] == candidate else 0
        return score

    def compute_candidate_scores(self, k, profile):
        profile.clean_scores()
        for pref in profile.preferences:
            pref_winner = pref.order[0]
            if pref_winner in profile.scores:
                profile.scores[pref_winner] += 1
            else:
                profile.scores[pref_winner] = 1
