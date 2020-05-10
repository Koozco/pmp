from typing import List, Tuple

from aaa_pb.rules.bruteforcetemplate import BruteForceRule
from aaa_pb.rules.ordinal.single_committee_value import CommitteeScore


class PAV_BruteForce:

    @classmethod
    def apply(clazz, V: List[List[int]], number_of_candidates: int, k: int) -> Tuple[List[List[int]], float]:

        return BruteForceRule.apply(
            V=V,
            number_of_candidates=number_of_candidates,
            k=k,
            scoreCommitteeFun=CommitteeScore.PAV
        )
