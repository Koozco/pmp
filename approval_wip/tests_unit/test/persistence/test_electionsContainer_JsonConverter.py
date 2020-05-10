from aaa_pb.persistence.json_converters.elections_container_json_converter import ElectionsContainer_JsonConverter
from test.persistence.sample_objects_for_tests import SampleObjectsForTests
from test.test_base import TestBase


class TestElectionsContainer_JsonConverter(TestBase):

    def test_writing_and_loading(self):
        # given

        container = SampleObjectsForTests._container1

        tmp_dir_path = self.get_tmp_dir()
        file_path = tmp_dir_path / "election_container"
        file_path.mkdir()

        # when
        data = ElectionsContainer_JsonConverter.to_json_dict(
            elections_container=container,
        )

        actual_container = ElectionsContainer_JsonConverter.from_json_dict(
            data=data
        )

        # then
        self.assertEqual(container, actual_container)
