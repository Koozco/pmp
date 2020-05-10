import unittest

from aaa_pb.rules.approval.cc import CC_BruteForce
from aaa_pb.rules.approval.ilp.owa import CC_ILP
from aaa_pb.rules.approval.single_committee_value import CommitteeScore
from test.test_commons.approval_brute_force_test_template import ApprovalBruteForceTestTemplate


class CC_ILP_Test(unittest.TestCase):

    def test_with_brute_force(self):
        ApprovalBruteForceTestTemplate(self).testOnSampleElections(
            testedRuleFun=CC_ILP.apply,
            committeeScoreFun=CommitteeScore.CC,
            bruteForceRuleFun=CC_BruteForce.apply)
