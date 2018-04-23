from .rule import Rule

class Borda(Rule):
    """Borda vote scoring rule."""

    def __init__(self, committee_size, candidates, preferences):
        Rule.__init__(self, committee_size, candidates, preferences)
        self.weights = self.__borda_weights(len(candidates))
        self.scores = {}

    @staticmethod
    def __borda_weights(size):
        weights = [size - i for i in range(1, size + 1)]
        return weights

    def compute_score(self, candidate):
        score = 0
        for pref in self.preferences:
            candidate_id = pref.order.index(candidate)
            score += pref.weights[candidate_id]
        return score

    def compute_candidate_scores(self):
        self.scores = self.__clean_scores()
        for pref in self.preferences:
            for i in range(0, len(self.candidates)):
                self.scores[pref.order[i]] += self.weights[i]

    # to arbitrate ties
    def get_committee(self, winners):
        return winners[:self.k]

    def find_committee(self):
        self.compute_candidate_scores()
        winners = sorted(self.scores, key=lambda x: self.scores[x], reverse=True)
        committee = get_committee(winners)
        return committee

    def copy_rule(self):
        return Borda(self.k, self.candidates, self.preferences)
