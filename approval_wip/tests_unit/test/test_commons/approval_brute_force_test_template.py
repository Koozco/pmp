import unittest

from test.test_commons.brute_force_test_template import BruteForceTestTemplate
from test.test_commons.approval_election_test_data_source import ApprovalElectionTestDataSource


class ApprovalBruteForceTestTemplate(BruteForceTestTemplate):

    def __init__(self, testcase: unittest.TestCase) -> None:
        super(ApprovalBruteForceTestTemplate, self).__init__(
            testcase=testcase,
            dataSource=ApprovalElectionTestDataSource()
        )
