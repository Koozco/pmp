from typing import List

from aaa_pb.legacy.old_experiment import OldExperiment
from aaa_pb.model.distribution_descriptor import DistributionDescriptor
from aaa_pb.model.distribution_descriptor_from_fs import DistributionDescriptorFromFs
from aaa_pb.model.euclidean_distribution_descriptor import EuclideanDistributionDescriptor
from aaa_pb.model.euclidean_election_datapoints import EuclideanElectionDatapoints


class EuclideanElectionDatapointsGenerator:
    """
    Generates 2D points representing voters and candidates according to specified data distributions

    Delagates calculations to `OldExperiment`
    """

    @staticmethod
    def fromDistributionDescriptor(distribution_descriptor: DistributionDescriptor) -> List[EuclideanElectionDatapoints]:
        # delegate to legacy `OldExperiment`

        if isinstance(distribution_descriptor, EuclideanDistributionDescriptor):
            number_of_distributions = distribution_descriptor.number_of_datapoint_distributions
            ret = []
            for _ in range(number_of_distributions):
                old = OldExperiment.fromCommandList(commands=distribution_descriptor.commands,
                                                           ballot_calc=None,
                                                           output_dir_path=None)
                old.run()
                x = EuclideanElectionDatapoints(
                    V=old.V,
                    C=old.C)
                ret.append(x)

            return ret

        if isinstance(distribution_descriptor, DistributionDescriptorFromFs):
            number_of_distributions = distribution_descriptor.number_of_distributions

            ret = []
            for idx in range(number_of_distributions):
                datapoints_file = distribution_descriptor.src_dir_path / str(idx)
                x = EuclideanElectionDatapoints.fromFile(datapoints_file_path=datapoints_file)
                ret.append(x)

            return ret

    pass
