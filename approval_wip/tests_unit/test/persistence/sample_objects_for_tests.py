from aaa_pb.model.ballot_2d2 import ApprovalBallotCalc_NearestUniform, ApprovalBallotCalc_RadiusUniform
from aaa_pb.model.election_instance import ElectionInstance
from aaa_pb.model.election_instance_container import ElectionInstancesContainer
from aaa_pb.model.euclidean_distribution_descriptor import EuclideanDistributionDescriptor


class SampleObjectsForTests:
    _election_instance1 = ElectionInstance(
        V=[(0.0, 0.1)] * 3,
        C=[(11.0, 2.1)] * 2,
        P=[[1, 2],
           [1],
           [1, 2, 3]
           ]
    )

    _election_instance2 = ElectionInstance(
        V=[(2.0, 0.1)] * 5,
        C=[(0.1, 0.1)] * 4,
        P=[[1, 3],
           [1, 4],
           [1, 2, 3],
           [4],
           [2]
           ]
    )

    _election_instance3 = ElectionInstance(
        V=[(0.0, 0.0)] * 5,
        C=[(0.0, 0.0)] * 4,
        P=[[1, 3],
           [2, 4],
           [1, 2, 3],
           [4],
           [2]
           ]
    )
    _descriptor1 = EuclideanDistributionDescriptor(
        commands=["this", "is", "list", "of commands"],
        label="this is a label",
        number_of_datapoint_distributions=123
    )

    _descriptor2 = EuclideanDistributionDescriptor(
        commands=["this", "is", "list", "of commands2"],
        label="this is a label2",
        number_of_datapoint_distributions=93
    )

    _ballot_calc1 = ApprovalBallotCalc_NearestUniform(min=10.0, max=111.11)
    _ballot_calc2 = ApprovalBallotCalc_RadiusUniform(min=10.0, max=111.11)

    _container1 = ElectionInstancesContainer(
        election_instances=[
            _election_instance1,
            _election_instance2
        ],
        ballot_calc=_ballot_calc1,
        distribution_descriptor=_descriptor1

    )

    _container2 = ElectionInstancesContainer(
        election_instances=[
            _election_instance1,
            _election_instance2,
            _election_instance3,
            _election_instance1,
        ],
        ballot_calc=_ballot_calc2,
        distribution_descriptor=_descriptor2

    )
