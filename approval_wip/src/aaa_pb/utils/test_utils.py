from pathlib import Path

from aaa_pb.directory_structure import DirectoryStructure


class TestUtils:

    @classmethod
    def _find_test_init_dir_path(self) -> Path:
        return DirectoryStructure.project_dir / 'tests_unit' / "test-input"
