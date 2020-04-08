from pathlib import Path
from typing import List, Tuple

from aaa_pb.model.distribution_descriptor_from_fs import DistributionDescriptorFromFs
from aaa_pb.model.euclidean_distribution_descriptor import EuclideanDistributionDescriptor
from aaa_pb.model.euclidean_election_datapoints import EuclideanElectionDatapoints


class EuclideanDistributionDescriptorContainer:
    # TODO simplify

    def __init__(self, descriptors: List[EuclideanDistributionDescriptor]) -> None:
        self.__descriptors = descriptors
        pass

    def getDescriptorList(self):
        return self.__descriptors

    @classmethod
    def toDir(cls, output_dir_path: Path, list_of_descriptors_and_list_of_datapoints: List[Tuple[EuclideanDistributionDescriptor, List[EuclideanElectionDatapoints]]]):

        info_file_content = []

        output_dir_path.mkdir(exist_ok=False, parents=True)

        for idx, (descriptor, datapoint_sets) in enumerate(list_of_descriptors_and_list_of_datapoints):
            info_file_content.append(
                str(idx) + ", " + descriptor.label + ", " + str(descriptor.number_of_datapoint_distributions))

            datapoints_dir = output_dir_path / str(idx)
            datapoints_dir.mkdir(parents=False, exist_ok=False)

            for dpidx, datapoint_set in enumerate(datapoint_sets):
                output_file_path = datapoints_dir / str(dpidx)
                datapoint_set.toFile(output_file_path=output_file_path)

        with open(str(output_dir_path / "info.txt"), 'w') as info_file:
            for line in info_file_content:
                print >> info_file, line
        pass

    @classmethod
    def fromDir(cls, input_dir_path: Path) -> 'EuclideanDistributionDescriptorContainer':
        info_file_path = input_dir_path / "info.txt"

        list_of_distribution_descriptors: List[DistributionDescriptorFromFs] = []

        with open(str(info_file_path), 'r') as info_file:
            lines = info_file.readlines()
            for line in lines:
                distribution_dir_name, label, number_of_distributions = [x.strip() for x in line.split(",")]
                list_of_distribution_descriptors.append(
                    DistributionDescriptorFromFs(
                        src_dir_path=input_dir_path / distribution_dir_name,
                        distribution_label=label,
                        number_of_distributions=int(number_of_distributions)
                    )
                )

        return EuclideanDistributionDescriptorContainer(list_of_distribution_descriptors)

    @classmethod
    def getByNames(clazz, names: List[str], number_of_voters_and_candidates: int, number_of_datapoint_distributions: int) -> 'EuclideanDistributionDescriptorContainer':
        ds = [d for d in clazz.getDefault(
            number_of_voters_and_candidates=number_of_voters_and_candidates,
            number_of_datapoint_distributions=number_of_datapoint_distributions).getDescriptorList() if
              d.label in names]
        return EuclideanDistributionDescriptorContainer(ds)

    @classmethod
    def getDefault(clazz, number_of_voters_and_candidates: int, number_of_datapoint_distributions: int) -> 'EuclideanDistributionDescriptorContainer':
        distributions = {
            'unisqua': ['candidates',
                        'uniform -3 -3 3 3 {0}'.format(number_of_voters_and_candidates),
                        'voters',
                        'uniform -3 -3 3 3 {0}'.format(number_of_voters_and_candidates),
                        ],
            'unidisc': ['candidates',
                        'circle 0 0 3 {0}'.format(number_of_voters_and_candidates),
                        'voters',
                        'circle 0 0 3 {0}'.format(number_of_voters_and_candidates)
                        ]
        }

        descriptors = []
        for label, commands in distributions.items():
            descriptors.append(
                EuclideanDistributionDescriptor(
                    commands=commands,
                    label=label,
                    number_of_datapoint_distributions=number_of_datapoint_distributions
                )
            )

        descriptors.append(
            EuclideanDistributionDescriptor.getGauss1(number_of_voters_and_candidates,
                                                      number_of_datapoint_distributions))
        descriptors.append(
            EuclideanDistributionDescriptor.getGauss4(number_of_voters_and_candidates,
                                                      number_of_datapoint_distributions))

        return EuclideanDistributionDescriptorContainer(descriptors)
