from typing import List, Dict, Any

from aaa_pb.model.election_instance_container import ElectionInstancesContainer
from aaa_pb.persistence.json_converters.elections_container_json_converter import ElectionsContainer_JsonConverter


class ListOfElectionsContainers_JsonConverter:

    @classmethod
    def to_json_dict(self, elections_containers: List[ElectionInstancesContainer]) -> Dict[str, Any]:
        election_container_list = []
        for i, elections_container in enumerate(elections_containers):
            election_container_list.append(
                ElectionsContainer_JsonConverter.to_json_dict(
                    elections_container=elections_container,
                )
            )
        data = {
            "number_of_elections_containers": len(elections_containers),
            "election_container_list": election_container_list
        }
        return data

    @classmethod
    def from_json_dict(self, data: Dict[str, Any]) -> List[ElectionInstancesContainer]:

        election_containers = []

        for election_container_data in data["election_container_list"]:
            elections_container = ElectionsContainer_JsonConverter.from_json_dict(
                data=election_container_data
            )
            election_containers.append(elections_container)
        return election_containers
