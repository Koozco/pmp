import unittest

from aaa_pb.rules.approval.pav import PAV_Genetic
from aaa_pb.rules.approval.single_committee_value import CommitteeScore
from aaa_pb.rules.approval.pav import PAV_BruteForce
from test.test_commons.trends_com_soc_data import TrendsComSoc_Data


class PAV_Genetic_Test(unittest.TestCase):

    def test_1(self):
        # when
        committee = TrendsComSoc_Data.call_rule_for_example_2_3(PAV_Genetic)

        # then
        expected_score = CommitteeScore.PAV(V=TrendsComSoc_Data.V_call_rule_for_example_2_3, committee=[0, 1])
        actual_score = CommitteeScore.PAV(V=TrendsComSoc_Data.V_call_rule_for_example_2_3, committee=committee)

        self.assertEqual(expected_score, actual_score)

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
        a_best_committee = [c, d]
        expected_score = CommitteeScore.PAV(V=V, committee=a_best_committee)

        # when
        actual = PAV_Genetic.apply(
            number_of_candidates=number_of_candidates,
            k=k,
            V=V)

        # then
        actual_score = CommitteeScore.PAV(V=V, committee=actual)

        brute_forced_committees, best_score = PAV_BruteForce.apply(V=V, number_of_candidates=number_of_candidates, k=k)
        brute_forced_committee_score = CommitteeScore.PAV(V=V, committee=brute_forced_committees[0])

        self.assertEqual(expected_score, actual_score)
        self.assertEqual(expected_score, brute_forced_committee_score)

        pass
