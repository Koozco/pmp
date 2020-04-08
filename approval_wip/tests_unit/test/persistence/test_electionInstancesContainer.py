from typing import List

from aaa_pb.model.election_instance_container import ElectionInstancesContainer
from aaa_pb.persistence.json_converters.list_of_election_containers_json_converter import \
    ListOfElectionsContainers_JsonConverter
from test.persistence.sample_objects_for_tests import SampleObjectsForTests
from test.test_base import TestBase


class ElectionInstancesContainerTest(TestBase):

    def test_writing_and_loading(self):
        # given
        container_list: List[ElectionInstancesContainer] = [
            SampleObjectsForTests._container1,
            SampleObjectsForTests._container2
        ]

        # when
        data = ListOfElectionsContainers_JsonConverter.to_json_dict(
            elections_containers=container_list,
        )
        actual = ListOfElectionsContainers_JsonConverter.from_json_dict(data=data)

        # then
        self.assertEqual(expected=container_list, actual=actual)
