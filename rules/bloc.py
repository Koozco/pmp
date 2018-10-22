from .weakly_separable import WeaklySeparable


class Bloc(WeaklySeparable):
    """Bloc vote scoring rule."""

    def find_committee(self, k, profile):
        self.weights = self._bloc_weights(k)
        committee = WeaklySeparable.find_committee(self, k, profile)
        return committee

    def compute_score(self, candidate, k, profile):
        self.weights = self._bloc_weights(k)
        score = WeaklySeparable.compute_score(self, candidate, k, profile)
        return score

    def _bloc_weights(self, k):
        return [1] * k

# class Bloc(WeaklySeparable):
#     """Bloc vote scoring rule."""
#
#     def __init__(self, committee_size):
#         WeaklySeparable.__init__(self, committee_size)
#
#     def __bloc_weights(self, size):
#         self.weights = [1] * self.k + [0] * (size - self.k)
#
#     def compute_score(self, candidate, candidates, preferences):
#         self.__bloc_weights(len(candidates))
#         score = 0
#         for pref in preferences:
#             score += 1 if pref.order[0] == candidate else 0
#         return score
#
#     def compute_candidate_scores(self, candidates, preferences):
#         self._clean_scores(candidates)
#         self.__bloc_weights(len(candidates))
#         for pref in preferences:
#             for i in range(0, self.k):
#                 self.scores[pref.order[i]] += self.weights[i]
#
#     def copy_rule(self):
#         return Bloc(self.k)
