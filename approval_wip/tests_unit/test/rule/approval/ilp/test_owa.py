import unittest

from aaa_pb.rules.approval.ilp.owa import PAV_ILP, CC_ILP
from test.test_commons.trends_com_soc_data import TrendsComSoc_Data


class PAV_ILP_Test(unittest.TestCase):

    def test_PAV(self):
        # when
        committee = TrendsComSoc_Data.call_rule_for_example_2_3(PAV_ILP)

        # then
        expectedCommittees = [[0, 1], [1, 2], [1, 3]]
        if committee not in expectedCommittees:
            self.assertListEqual(committee, expectedCommittees[0])

    def test_CC(self):
        # Approval-Based Chamberlin-Courant rule (alpha-CC). Under the alpha-CC rule we use
        # vectors of the form (1, 0, . . . , 0). As in the case of the ordinal-based
        # Chamberlin-Courant rule (beta-CC), a possible interpretation is that each voter
        # chooses a representative from the committee and, thus, increases the score
        # of the committee by one if there is at least one committee member that this
        # voter approves.

        # The winning committee under a-CC is {a, b} (with score five, where only v 3 does not approve any committee member)

        # when
        actual_committee = TrendsComSoc_Data.call_rule_for_example_2_3(CC_ILP)

        # then
        expected_committee1 = [0, 1]
        expected_committee2 = [1, 3]

        self.assertIn(actual_committee, [expected_committee1, expected_committee2])
