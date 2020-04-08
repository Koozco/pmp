import unittest
from typing import Callable

from aaa_pb.utils.misc_utils import MiscUtils
from test.test_commons.election_test_data_source import ElectionTestDataSource


class BruteForceTestTemplate:

    def __init__(self, testcase: unittest.TestCase, dataSource: ElectionTestDataSource) -> None:
        self.testcase = testcase
        self.dataSource = dataSource

    def testOnSampleElections(self, testedRuleFun: Callable, committeeScoreFun: Callable, bruteForceRuleFun: Callable) -> None:
        """
        :param testedRuleFun: (V, ?number_of_candidates, k) -> list[int]
        :param committeeScoreFun: (V, actualCommittee) -> float
        :param bruteForceRuleFun:  (V, ?number_of_candidates, k) -> list[list[int]], float
        """
        for electionDataDict in self.dataSource.getSampleElections():
            # given
            V, number_of_candidates, k = MiscUtils.pluck(electionDataDict, 'V', 'number_of_candidates', 'k')

            # expected
            expectedCommittees, expectedScore = bruteForceRuleFun(V=V, number_of_candidates=number_of_candidates, k=k)

            # when
            actualCommittee = testedRuleFun(V=V, number_of_candidates=number_of_candidates, k=k)
            actualScore = committeeScoreFun(V=V, committee=actualCommittee)

            # then
            self.testcase.assertIn(
                member=actualCommittee,
                container=expectedCommittees,
                msg="{0} with score {1} not in {2} with score {3}".format(
                    actualCommittee,
                    actualScore,
                    expectedCommittees,
                    expectedScore)
            )
            self.testcase.assertEqual(expectedScore, actualScore)

    pass
