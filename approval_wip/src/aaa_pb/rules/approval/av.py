from typing import List

from aaa_pb.rules.approval_based_rule_base import ApprovalBasedRuleBase


class AV(ApprovalBasedRuleBase):

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:

        number_of_votes_per_candidate = [0] * number_of_candidates

        for vote in V:
            for c in vote:
                number_of_votes_per_candidate[c] += 1

        candidates = list(range(number_of_candidates))
        clazz.randomUtils.shuffle(candidates)
        candidates_best_to_worst = sorted(candidates, key=lambda c: -number_of_votes_per_candidate[c])
        committee = candidates_best_to_worst[:k]
        return committee

