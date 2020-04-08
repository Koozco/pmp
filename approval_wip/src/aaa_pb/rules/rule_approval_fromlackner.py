from typing import List

import core
import rules.lackner_approval
import rules.lackner_preference
import rules.lackner_profile
import rules.rule_approval

from rules import lackner_preference, lackner_profile, lackner_approval
from rules.approval_based_rule_base import ApprovalBasedRuleBase

core.RULES += [("RAV_Lackner"), ""]
core.RULES += [("seqMaxPhragmen_Lackner"), ""]


class RAV_Lackner(ApprovalBasedRuleBase):

    @classmethod
    def apply(cls, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:
        def getDP(votes: List[int]):
            return lackner_preference.DichotomousPreference(votes, number_of_candidates)

        profile = lackner_profile.Profile(number_of_candidates)
        for votes in V:
            dp = getDP(votes)
            profile.add_preference(dp)

        committee = lackner_approval.compute_seqpav(
            profile=profile,
            committeesize=k,
            tiebreaking=True)

        return list(committee[0])


class SeqMaxPhragmen_Lackner(ApprovalBasedRuleBase):

    @classmethod
    def apply(cls, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:
        # todo pass exact number of candidates!
        index_of_biggest_candidate = max([max(v) for v in V])
        n = index_of_biggest_candidate + 1  # approximate number of candidates

        def getDP(votes: List[int]):
            return lackner_preference.DichotomousPreference(votes, n)

        profile = lackner_profile.Profile(n)
        for votes in V:
            dp = getDP(votes)
            profile.add_preference(dp)

        committee = lackner_approval.compute_seqphragmen(
            profile=profile,
            committeesize=k
        )

        return list(committee[0])
