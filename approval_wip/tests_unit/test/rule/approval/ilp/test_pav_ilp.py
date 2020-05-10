import unittest

from aaa_pb.rules.approval.ilp.owa import PAV_ILP
from aaa_pb.rules.approval.pav import PAV_BruteForce
from aaa_pb.rules.approval.single_committee_value import CommitteeScore
from test.test_commons.approval_brute_force_test_template import ApprovalBruteForceTestTemplate


class PAV_ILP_Test(unittest.TestCase):

    def test_with_brute_force(self):
        ApprovalBruteForceTestTemplate(self).testOnSampleElections(
            testedRuleFun=PAV_ILP.apply,
            committeeScoreFun=CommitteeScore.PAV,
            bruteForceRuleFun=PAV_BruteForce.apply)
