from typing import List


class CommitteeScore():

    @classmethod
    def PAV(cls, V: List[List[int]], committee: List[int]) -> float:

        k = len(committee)

        owa = [1.0 / i for i in range(1, k + 1)]
        committee = set(committee)

        score = 0.0

        for vote in V:
            vote = set(vote)
            number_of_supported_candidates = len(committee.intersection(vote))
            score += sum(owa[:number_of_supported_candidates])

        return score

    @classmethod
    def CC(cls, V: List[List[int]], committee: List[int]) -> float:
        committee = set(committee)

        score = 0

        for vote in V:
            vote = set(vote)
            if len(committee.intersection(vote)) > 0:
                score += 1

        return score
