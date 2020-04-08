from typing import List, Tuple, Any

from aaa_pb.model.ballot_calc import BallotCalc
from aaa_pb.model.euclidean_election_datapoints import EuclideanElectionDatapoints


class ElectionInstance:

    def __init__(self,
                 V: List[Tuple[float, float]],
                 C: List[Tuple[float, float]],
                 P: List[List[int]]) -> None:
        self.V = V
        self.C = C
        self.P = P
        assert len(C) > 0
        assert isinstance(C[0],
                          Tuple), f"Candidates should be tuples2 of float but actual is '{C[0]}' of type {type(C[0])}"
        pass

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ElectionInstance):
            return self.V == other.V \
                   and self.C == other.C \
                   and self.P == self.P
        else:
            return False

    def __hash__(self) -> int:
        tuple = (self.V, self.C, self.P)
        return hash(tuple)

    def __str__(self) -> str:
        V_str = " ".join([str(x) for x in self.V])
        C_str = " ".join([str(x) for x in self.C])
        profiles_list = []
        for profile in self.P:
            profiles_list.append(" ".join([str(x) for x in profile]))
        profiles_str = "\n".join(profiles_list)

        return "V: {}\nC: {}:\nP:\n{}".format(V_str, C_str, profiles_str)

    def __repr__(self) -> str:
        return self.__str__()

    def getNumberOfCandidates(self) -> int:
        return len(self.C)

    @staticmethod
    def fromEuclideanDatapoints(euclidean_election_datapoints: EuclideanElectionDatapoints,
                                ballot_calc: BallotCalc) -> 'ElectionInstance':

        P = ballot_calc.calculateFrom2dPoints(
            V=euclidean_election_datapoints.V,
            C=euclidean_election_datapoints.C
        )

        return ElectionInstance(
            V=euclidean_election_datapoints.V,
            C=euclidean_election_datapoints.C,
            P=P
        )
