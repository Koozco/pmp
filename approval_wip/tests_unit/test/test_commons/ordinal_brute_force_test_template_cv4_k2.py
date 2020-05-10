import unittest

from test.test_base import TestBase
from test.test_commons.brute_force_test_template import BruteForceTestTemplate
from test.test_commons.ordinal_election_test_data_source import OrdinalElectionTestDataSource


# TODO duplication with OrdinalBruteForceTestTemplate_CV12
class OrdinalBruteForceTestTemplate_CV4_k2(BruteForceTestTemplate):

    def __init__(self, testcase: unittest.TestCase) -> None:
        dataSource = OrdinalElectionTestDataSource(
            data_dir=TestBase.TEST_INIT_DIR_PATH / "ordinal-cv4_20181104-213844",
            # file_names=[str(x) for x in range(1, 11)]
            file_names=[str(x) for x in [1]],
            k=2
        )
        super(OrdinalBruteForceTestTemplate_CV4_k2, self).__init__(
            testcase=testcase,
            dataSource=dataSource
        )
