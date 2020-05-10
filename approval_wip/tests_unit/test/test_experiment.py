import unittest

from aaa_pb.model.euclidean_distribution_descriptor import EuclideanDistributionDescriptor
from aaa_pb.model.euclidean_election_datapoints import EuclideanElectionDatapoints
from aaa_pb.model.euclidean_election_datapoints_generator import EuclideanElectionDatapointsGenerator
from test.test_base import TestBase


class EuclideanElectionDatapointsGenerator_Test(TestBase):

    @unittest.skip("Test impl ongoing")
    def test_dataPointGeneration(self):
        # given
        distribution_descriptor = EuclideanDistributionDescriptor(
            commands=['candidates',
                      'circle 0 0 3 200',
                      'voters',
                      'circle 0 0 3 200'
                      ],
            label="label")

        # when
        actual = EuclideanElectionDatapointsGenerator \
            .fromDistributionDescriptor(distribution_descriptor)

        # then
        self.assertTrue(
            isinstance(actual, EuclideanElectionDatapoints))

        self.assertEqual(len(actual.C), 200)
        self.assertEqual(len(actual.V), 200)

        self.assertEqual(type(actual.C[0]), tuple)
        self.assertEqual(type(actual.V[0]), tuple)

        self.assertEqual(type(actual.V[0][0]), float)
        self.assertEqual(type(actual.V[0][1]), float)

        self.assertEqual(type(actual.C[0][0]), float)
        self.assertEqual(type(actual.C[0][1]), float)

        pass


