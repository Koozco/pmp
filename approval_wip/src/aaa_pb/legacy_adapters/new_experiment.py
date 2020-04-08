from typing import Type

from aaa_pb.legacy_adapters.winner_adapter import Winner_Adapter
from aaa_pb.model.election_instance import ElectionInstance
from aaa_pb.model.election_result import ElectionResult
from rules.approval_based_rule_base import ApprovalBasedRuleBase


class NewExperiment:

    @staticmethod
    def computeElectionResult(
            election_instance: ElectionInstance,
            rule_class: Type[ApprovalBasedRuleBase],
            committee_size: int) -> ElectionResult:

        W = Winner_Adapter().calculateWinnerSane(
            V=election_instance.P,
            number_of_candidates=election_instance.getNumberOfCandidates(),
            k=committee_size,
            rule_class=rule_class
        )

        return ElectionResult(
            election_instance=election_instance,
            committee=W,
            rule_class=rule_class
        )

    pass
