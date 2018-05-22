from .weakly_separable import WeaklySeparable

class Bloc(WeaklySeparable):
    """Bloc vote scoring rule."""

    def __init__(self, k):
        weights = [1] * k
        WeaklySeparable.__init__(self, k, weights)


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
