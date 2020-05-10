from typing import List, Any, Tuple

from aaa_pb.model.ballot_calc import BallotCalc
from aaa_pb.model.euclidean_distribution_descriptor import EuclideanDistributionDescriptor
from aaa_pb.model.euclidean_election_datapoints import EuclideanElectionDatapoints
from aaa_pb.model.election_instance import ElectionInstance


class ElectionInstancesContainer:

    #     def serializeToString(self):
    #
    #         ballot_calc_dict = self.ballot_calc.to_dict()
    #
    #         serialized_distribution_descriptor = self.distribution_descriptor.serializeToString()
    #         number_of_serialized_instances = len(self.election_instances)
    #         serialized_instances = "\n".join([x.serializeToString() for x in self.election_instances])
    #
    #         """{0}
    # {1}
    # {2}
    # {3}""".format(serialized_ballot_calc,
    #               serialized_distribution_descriptor,
    #               str(number_of_serialized_instances),
    #               serialized_instances)
    #
    #         pass
    #
    #     @classmethod
    #     def deserializeFromString(clazz, s):
    #         lines = s.splitlines()
    #         number_of_elections = int(lines[0])
    #         lines = lines[1:]
    #
    #         ballot_calc, lines = ballot_2d2.BallotCalc.deserializeFromLines(lines)
    #         distribution_descriptor, lines = EuclideanDistributionDescriptor.deserializeFromLines(s)
    #
    #         number_of_instances = int(lines[0])
    #         lines = lines[1:]
    #
    #         deserialized_instances = []
    #         for _ in range(number_of_instances):
    #             deserialized_instance, lines = ElectionInstance.deserializeFromLines(lines)
    #             deserialized_instances.append(deserialized_instance)
    #
    #         return ElectionInstancesContainer(
    #             election_instances=deserialized_instances,
    #             ballot_calc=ballot_calc,
    #             distribution_descriptor=distribution_descriptor
    #         )

    def __init__(self,
                 election_instances: List[ElectionInstance],
                 ballot_calc: BallotCalc,
                 distribution_descriptor: EuclideanDistributionDescriptor) -> None:
        self.election_instances = election_instances
        self.ballot_calc = ballot_calc
        self.distribution_descriptor = distribution_descriptor

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ElectionInstancesContainer):
            return other.distribution_descriptor == self.distribution_descriptor \
                   and other.ballot_calc == self.ballot_calc \
                   and other.election_instances == self.election_instances
        else:
            return False

    def getBallotCalcLabel(self) -> str:
        return self.ballot_calc.getShortName()

    @classmethod
    def fromDistribution(
            cls,
            distribution_descriptor: EuclideanDistributionDescriptor,
            ballot_calcs: List[BallotCalc],
            list_of_datapoints: List[EuclideanElectionDatapoints]) -> List['ElectionInstancesContainer']:

        election_instances_list: List[Tuple[BallotCalc, List[ElectionInstance]]] = cls.__generate_election_instances(
            ballot_calcs=ballot_calcs,
            list_of_datapoints=list_of_datapoints
        )

        result = []
        for ballot_calc, election_instances in election_instances_list:
            result.append(
                ElectionInstancesContainer(
                    election_instances=election_instances,
                    ballot_calc=ballot_calc,
                    distribution_descriptor=distribution_descriptor
                )
            )
        return result

    @classmethod
    def __generate_election_instances(
            cls,
            ballot_calcs: List[BallotCalc],
            list_of_datapoints: List[EuclideanElectionDatapoints]) -> List[Tuple[BallotCalc, List[ElectionInstance]]]:

        def create_election_instance(
                euclidean_election_datapoints: EuclideanElectionDatapoints,
                ballot_calc: BallotCalc) -> ElectionInstance:
            return ElectionInstance.fromEuclideanDatapoints(
                euclidean_election_datapoints=euclidean_election_datapoints,
                ballot_calc=ballot_calc)

        euclidean_election_datapoints_list = list_of_datapoints

        election_instances_list = []

        for ballot_calc in ballot_calcs:
            election_instances = []

            for x in euclidean_election_datapoints_list:
                election_instances.append(
                    create_election_instance(
                        euclidean_election_datapoints=x,
                        ballot_calc=ballot_calc
                    )
                )

            election_instances_list.append(
                (
                    ballot_calc,
                    election_instances
                )
            )

        return election_instances_list
