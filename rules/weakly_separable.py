from .rule import Rule


class WeaklySeparable(Rule):
    """ Weakly Separable scoring rule """

    def __init__(self, weights=None):
        Rule.__init__(self)
        self.weights = weights

    def compute_candidate_scores(self, k, profile):
        for pref in profile.preferences:
            for n in range(len(pref.order)):
                candidate = pref.order[n]
                weight = self.weights[n] if n < len(self.weights) else 0
                profile.scores[candidate] += weight

    def compute_score(self, candidate, k, profile):
        score = 0
        for pref in profile.preferences:
            i = pref.order.index(candidate)
            weight = self.weights[i] if i < len(self.weights) else 0
            score += weight
        return score

    # function to arbitrate ties
    def get_committee(self, k, winners):
        return [w for w in winners[:k]]

    def find_committee(self, k, profile):
        if self.weights is None:
            raise Exception("Weights not set.")
        profile.clean_scores()
        self.compute_candidate_scores(k, profile)

        winners = sorted(profile.candidates, key=lambda x: profile.scores[x], reverse=True)
        committee = self.get_committee(k, winners)
        return committee
