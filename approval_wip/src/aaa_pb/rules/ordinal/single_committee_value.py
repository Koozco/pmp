from typing import List


class CommitteeScore:

    @classmethod
    def PAV(cls, V: List[List[int]], committee: List[int]) -> float:

        k = len(committee)

        owa = [1.0 / i for i in range(1, k + 1)]
        committee = set(committee)

        score = 0.0

        for vote in V:
            top_k_candidates = set(vote[:k])
            number_of_supported_candidates = len(committee.intersection(top_k_candidates))
            score += sum(owa[:number_of_supported_candidates])

        return score
