from .algorithm import Algorithm


class Greedy(Algorithm):
    """Greedy algorithm - k-times takes best candidate."""

    def __init__(self, rule):
        Algorithm.__init__(self, rule)
        self.name = "Greedy"

    def find_committee(self):
        committee = []
        left_candidates = list(self.rule.candidates)
        for i in range(self.rule.k):
            best_candidate = None
            best_score = -1

            for c in left_candidates:
                score = self.rule.compute_score(c)
                if score > best_score:
                    best_score = score
                    best_candidate = c

            committee.append(best_candidate)
            left_candidates.remove(best_candidate)

        return committee

    def set_algorithm(self):
        self.rule.algorithm = self
        self.rule.find_committee = self.find_committee
        return self.rule
