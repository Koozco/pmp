from .weakly_separable import WeaklySeparable


class SNTV(WeaklySeparable):
    """Single non-transferable vote scoring rule."""

    def __init__(self, k):
        WeaklySeparable.__init__(self, k, [1])

    def compute_score(self, candidate, profile):
        score = 0
        for pref in profile.preferences:
            score += 1 if pref.order[0] == candidate else 0
        return score

    def compute_candidate_scores(self, profile):
        profile.clean_scores()
        for pref in profile.preferences:
            pref_winner = pref.order[0]
            profile.scores[pref_winner] += 1
