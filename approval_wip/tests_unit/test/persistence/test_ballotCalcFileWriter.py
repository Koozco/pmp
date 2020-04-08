from aaa_pb.persistence.json_converters.ballot_calc_file_writer import ApprovalBallotCalc_JsonConverter
from test.persistence.sample_objects_for_tests import SampleObjectsForTests
from test.test_base import TestBase


class BallotCalcFileWriterTest(TestBase):

    def test_writing_and_loading(self):
        # given
        ballot_calc = SampleObjectsForTests._ballot_calc1

        # when
        data = ApprovalBallotCalc_JsonConverter.persist(
            calc=ballot_calc,
        )
        print(data)
        actual_calc = ApprovalBallotCalc_JsonConverter.load(
            data=data
        )

        # then
        self.assertEqual(expected=ballot_calc, actual=actual_calc)
