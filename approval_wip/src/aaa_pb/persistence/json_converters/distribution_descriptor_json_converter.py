from typing import Dict, Any

from aaa_pb.model.euclidean_distribution_descriptor import EuclideanDistributionDescriptor


class DistributionDescriptor_JsonConverter:
    @classmethod
    def to_json_dict(self, descriptor: EuclideanDistributionDescriptor) -> Dict[str, Any]:
        data = {
            "label": descriptor.label,
            "number_of_distributions": descriptor.number_of_datapoint_distributions,
            "commands": descriptor.commands
        }
        return data


    @classmethod
    def from_json_dict(self, data: Dict[str, Any]) -> EuclideanDistributionDescriptor:
        return EuclideanDistributionDescriptor(
            commands=data["commands"],
            label=data["label"],
            number_of_datapoint_distributions=data["number_of_distributions"]
        )
