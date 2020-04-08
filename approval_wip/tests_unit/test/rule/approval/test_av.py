import unittest

from test.test_commons.trends_com_soc_data import TrendsComSoc_Data


class AV_Test(unittest.TestCase):

    def test_AV(self):
        from aaa_pb.rules.approval.av import AV


        # when
        commitee = TrendsComSoc_Data.call_rule_for_example_2_3(AV)

        # then
        self.assertListEqual(commitee, [1, 2])
