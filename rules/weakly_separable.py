from .rule import Rule


class WeaklySeparable(Rule):
    """ Weakly Separable scoring rule """

    def __init__(self, committee_size, candidates, preferences):
        Rule.__init__(self, committee_size, candidates, preferences)
        self.weights = [0] * len(candidates)
        self.scores = self.__clean_scores()

    def __clean_scores(self):
        return {candidate: 0 for candidate in self.candidates}

    # function to arbitrate ties
    def get_committee(self, winners):
        return winners[:self.k]

    def find_committee(self):
        self.compute_candidate_scores()
        winners = sorted(self.scores, key=lambda x: self.scores[x], reverse=True)
        committee = self.get_committee(winners)
        return committee
