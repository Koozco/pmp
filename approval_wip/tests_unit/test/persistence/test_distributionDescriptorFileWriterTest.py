from aaa_pb.persistence.json_converters.distribution_descriptor_json_converter import \
    DistributionDescriptor_JsonConverter
from test.persistence.sample_objects_for_tests import SampleObjectsForTests
from test.test_base import TestBase


class DistributionDescriptorFileWriterTest(TestBase):

    def test_writing_and_loading(self) -> None:
        # given
        descriptor = SampleObjectsForTests._descriptor1


        # when
        data = DistributionDescriptor_JsonConverter.to_json_dict(
            descriptor=descriptor
        )
        print(data)

        actual = DistributionDescriptor_JsonConverter.from_json_dict(
            data=data
        )

        # then
        self.assertEqual(expected=descriptor, actual=actual)
