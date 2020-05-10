import unittest

import aaa_pb.model.election_instance
from aaa_pb.model.ballot_2d2 import ApprovalBallotCalc_NearestUniform
from aaa_pb.model.euclidean_election_datapoints import EuclideanElectionDatapoints


class ElectionInstanceTest(unittest.TestCase):

    def test_ElectionInstance(self):
        # given
        datapoints = EuclideanElectionDatapoints(
            V=[(0, 10), (0, 0)],
            C=[(0, 1), (0, 2), (0, 11), (0, 12)]
        )

        # when
        actual = aaa_pb.model.election_instance.ElectionInstance. \
            fromEuclideanDatapoints(
            euclidean_election_datapoints=datapoints,
            ballot_calc=ApprovalBallotCalc_NearestUniform(min=2, max=2)
        )

        # then
        self.assertEqual(actual.C, [(0, 1), (0, 2), (0, 11), (0, 12)])
        self.assertEqual(actual.V, [(0, 10), (0, 0)])
        self.assertEqual(actual.P, [[2, 3], [0, 1]])
