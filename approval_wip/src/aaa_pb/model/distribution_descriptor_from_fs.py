from pathlib import Path

from aaa_pb.model.distribution_descriptor import DistributionDescriptor


class DistributionDescriptorFromFs(DistributionDescriptor):

    def __init__(self, src_dir_path: Path, distribution_label: str, number_of_distributions: int) -> None:
        self.src_dir_path = src_dir_path
        self.distribution_label = distribution_label
        self.number_of_distributions = number_of_distributions

    def getLabel(self) -> str:
        return self.distribution_label
