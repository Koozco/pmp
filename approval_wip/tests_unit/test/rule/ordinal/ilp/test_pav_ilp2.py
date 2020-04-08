import unittest

import pytest

from aaa_pb.rules.ordinal.ilp.pav_ilp import PAV_ILP_ordinal
from aaa_pb.rules.ordinal.pav import PAV_BruteForce
from aaa_pb.rules.ordinal.single_committee_value import CommitteeScore
from test.test_commons.ordinal_brute_force_test_template_cv12_k4 import OrdinalBruteForceTestTemplate_CV12_k4
from test.test_commons.ordinal_brute_force_test_template_cv4_k2 import OrdinalBruteForceTestTemplate_CV4_k2


class PAV_ILP_Test2(unittest.TestCase):

    @unittest.skip("harmonic borda")
    @pytest.mark.skip(reason="ala123")
    def test_with_brute_force_cv12_k4(self):
        OrdinalBruteForceTestTemplate_CV12_k4(
            testcase=self
        ).testOnSampleElections(
            testedRuleFun=PAV_ILP_ordinal.apply,
            committeeScoreFun=CommitteeScore.PAV,
            bruteForceRuleFun=PAV_BruteForce.apply)
        pass

    @unittest.skip("harmonic borda")
    @pytest.mark.skip(reason="ala123")
    def test_with_brute_force_cv4_k2(self):
        OrdinalBruteForceTestTemplate_CV4_k2(
            testcase=self
        ).testOnSampleElections(
            testedRuleFun=PAV_ILP_ordinal.apply,
            committeeScoreFun=CommitteeScore.PAV,
            bruteForceRuleFun=PAV_BruteForce.apply)
        pass
