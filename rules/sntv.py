from .weakly_separable import WeaklySeparable


class SNTV(WeaklySeparable):
    """Single non-transferable vote scoring rule."""

    def __init__(self, committee_size):
        WeaklySeparable.__init__(self, committee_size)

    def __clean_scores(self, candidates):
        self.scores = {candidate: 0 for candidate in candidates}

    def compute_score(self, candidate, candidates, preferences):
        score = 0
        for pref in preferences:
            score += 1 if pref.order[0] == candidate else 0
        return score

    def compute_candidate_scores(self, candidates, preferences):
        self.__clean_scores(candidates)
        for pref in preferences:
            pref_winner = pref.order[0]
            self.scores[pref_winner] += 1

    def copy_rule(self):
        return SNTV(self.k)
