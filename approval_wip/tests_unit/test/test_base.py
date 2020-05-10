import datetime
import unittest
from pathlib import Path
from typing import Any

from aaa_pb.directory_structure import DirectoryStructure
from aaa_pb.utils.test_utils import TestUtils


class TestBase(unittest.TestCase):
    TEST_INIT_DIR_PATH = TestUtils._find_test_init_dir_path()


    @classmethod
    def setUp(self) -> None:
        DirectoryStructure.TARGET_DIR.mkdir(exist_ok=True)

    def get_tmp_dir(self) -> Path:
        target_dir = DirectoryStructure.TARGET_DIR
        now = datetime.datetime.now()
        date_time_string = now.strftime("%Y%m%d-%H%M%S-%f")
        tmp_dir_path = target_dir / self.__class__.__name__ / date_time_string / self._get_current_test_method_name()
        tmp_dir_path.mkdir(parents=True, exist_ok=False)
        return tmp_dir_path

    def assertEqual(self, expected: Any, actual: Any) -> None:
        super().assertEqual(expected, actual)

    def _get_current_test_method_name(self) -> str:
        return self._testMethodName
