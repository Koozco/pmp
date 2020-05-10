from pathlib import Path
from typing import List

from aaa_pb.model.election_instance_container import ElectionInstancesContainer
from aaa_pb.persistence.json_converters.list_of_election_containers_json_converter import \
    ListOfElectionsContainers_JsonConverter
from aaa_pb.utils.json_utils import JsonUtils


class ListOfElectionsContainers_Persistence:

    @classmethod
    def persist(cls, path: Path, elections_containers: List[ElectionInstancesContainer]) -> None:
        data_dict = ListOfElectionsContainers_JsonConverter.to_json_dict(elections_containers=elections_containers)
        JsonUtils.write_json_file(
            path=path,
            data=data_dict
        )
