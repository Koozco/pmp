from typing import List

from aaa_pb.model.distribution_descriptor import DistributionDescriptor


class EuclideanDistributionDescriptor(DistributionDescriptor):

    @classmethod
    def getGauss1(cls, number_of_voters_and_candidates: int,
                  number_of_datapoint_distributions: int) -> 'EuclideanDistributionDescriptor':
        return EuclideanDistributionDescriptor(
            commands=cls.get2dGaussianElectionDistributionCommands(0, 0, 1, number_of_voters_and_candidates),
            label='gauss1',
            number_of_datapoint_distributions=number_of_datapoint_distributions
        )

    @classmethod
    def getGauss4(clazz, number_of_voters_and_candidates,
                  number_of_datapoint_distributions) -> 'EuclideanDistributionDescriptor':
        assert number_of_voters_and_candidates % 4 == 0
        c = number_of_voters_and_candidates / 4
        commands = (clazz.get2dGaussianElectionDistributionCommands(-1, 0, 0.5, c) +
                    clazz.get2dGaussianElectionDistributionCommands(1, 0, 0.5, c) +
                    clazz.get2dGaussianElectionDistributionCommands(0, -1, 0.5, c) +
                    clazz.get2dGaussianElectionDistributionCommands(0, 1, 0.5, c))
        return EuclideanDistributionDescriptor(
            commands=commands,
            label='gauss4',
            number_of_datapoint_distributions=number_of_datapoint_distributions
        )

    def __init__(self, commands: List[str], label: str, number_of_datapoint_distributions: int) -> None:
        self.label = label
        self.commands = commands
        self.number_of_datapoint_distributions = number_of_datapoint_distributions

    def __str__(self):
        commands_str = ", ".join(self.commands)
        return "EuclideanDistributionDescriptor(label={}, number_of_datapoint_distributions={}, commands={}" \
            .format(self.label, self.number_of_datapoint_distributions, commands_str)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, EuclideanDistributionDescriptor):
            return self.number_of_datapoint_distributions == other.number_of_datapoint_distributions \
                   and self.label == other.label \
                   and self.commands == self.commands
        pass

    def __hash__(self) -> int:
        return hash((self.number_of_datapoint_distributions, self.label, self.commands))

    @staticmethod
    def get2dGaussianElectionDistributionCommands(x: float, y: float, sigma: float, n: int) -> List[str]:
        distribution_str = 'gauss {0} {1} {2} {3}'.format(x, y, sigma, n)
        return [
            'candidates',
            distribution_str,
            'voters',
            distribution_str,
        ]
