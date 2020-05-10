import unittest

from aaa_pb.rules.approval.ilp.pav_sp_tu import PAV_SinglePeaked_ILP
from aaa_pb.rules.approval.pav import PAV_BruteForce
from aaa_pb.rules.approval.single_committee_value import CommitteeScore
from test.test_commons.approval_brute_force_test_template import ApprovalBruteForceTestTemplate
from test.test_commons.trends_com_soc_data import TrendsComSoc_Data


class PAV_SinglePeaked_ILP_Test(unittest.TestCase):

    def test_1(self):
        # when
        committee = TrendsComSoc_Data.call_rule_for_example_2_3(PAV_SinglePeaked_ILP)

        # then
        expectedCommittees = [[0, 1], [1, 2], [1, 3]]
        if committee not in expectedCommittees:
            self.assertListEqual(committee, expectedCommittees[0])

    # Data from
    # """
    # Single-Peakedness and Total Unimodularity:
    # ...
    # Dominik Peters
    # """
    def test_2(self):
        # given
        a = 0
        b = 1
        c = 2
        d = 3
        V = [
            [a, b, c],
            [c, d]
        ]
        k = 2
        number_of_candidates = 4
        expected1 = [c, d]
        expected2 = [a, c]

        # when
        actual = PAV_SinglePeaked_ILP.apply(
            number_of_candidates=number_of_candidates,
            k=k,
            V=V)

        #
        actual_score = CommitteeScore.PAV(V=V, committee=actual)
        expected1_score = CommitteeScore.PAV(V=V, committee=expected1)
        expected2_score = CommitteeScore.PAV(V=V, committee=expected2)
        self.assertEqual(expected1_score, actual_score)
        self.assertEqual(expected2_score, actual_score)
        if actual != expected1:
            self.assertListEqual(expected2, actual)

        pass

    def test_with_brute_force(self):
        ApprovalBruteForceTestTemplate(self).testOnSampleElections(
            testedRuleFun=PAV_SinglePeaked_ILP.apply,
            committeeScoreFun=CommitteeScore.PAV,
            bruteForceRuleFun=PAV_BruteForce.apply
        )
