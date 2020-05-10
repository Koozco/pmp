from aaa_pb.persistence.json_converters.election_instance_json_converter import ElectionInstance_JsonConverter
from test.persistence.sample_objects_for_tests import SampleObjectsForTests
from test.test_base import TestBase


class ElectionInstanceFileWriterTest(TestBase):

    def test_writing_and_loading(self):
        # given
        expected = SampleObjectsForTests._election_instance1
        tmp_dir = self.get_tmp_dir() / 'out.json'

        # when
        data = ElectionInstance_JsonConverter.to_json_dict(
            election=expected,
        )
        actual = ElectionInstance_JsonConverter.from_json_dict(
            data=data
        )

        # then
        self.assertEqual(expected=expected, actual=actual)
