import itertools
from typing import List, Callable, Collection, Iterable, Iterator


class BruteForceRule:

    @classmethod
    def apply(clazz,
              V: List[List[int]],
              number_of_candidates: int,
              k: int,
              scoreCommitteeFun: Callable[
                  [
                      List[List[int]],
                      List[int]
                  ], float]):
        """
        :param scoreCommitteeFun: (V, committee) -> float
        """

        def subsetsIter(S: Iterable[int], m: int) -> Iterator[List[int]]:
            # S - set
            # m - size of a subsets
            # return set(itertools.combinations(S, m))
            return itertools.combinations(S, m)

        best_committees = []
        best_score = -1

        for committee in subsetsIter(S=range(number_of_candidates), m=k):
            committee = list(committee)
            score = scoreCommitteeFun(V, committee)
            if score > best_score:
                best_score = score
                best_committees = [committee]
            elif score == best_score:
                best_committees.append(committee)

        return best_committees, best_score
