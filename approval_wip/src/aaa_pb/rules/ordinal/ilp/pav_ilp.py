from typing import List

from aaa_pb.legacy_rules import rule_proportional
from aaa_pb.rules.approval_based_rule_base import ApprovalBasedRuleBase


# from rules.rule_proportional import




# TODO create a common class for ordinal based elections
class PAV_ILP_ordinal(ApprovalBasedRuleBase):

    # eclude from approval rules because it's an ordinal rule
    excluded = True

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:

        owa = [1.0 / i for i in range(1, k + 1)]


        committee = rule_proportional.PAV(V, k)
        return committee


class PAV_ILP_ordinal2(ApprovalBasedRuleBase):

    # eclude from approval rules because it's an ordinal rule
    excluded = True

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> List[int]:
        owa = [1.0 / i for i in range(1, k + 1)]

        committee = rule_proportional.PAVtopk(V, k)
        return committee
