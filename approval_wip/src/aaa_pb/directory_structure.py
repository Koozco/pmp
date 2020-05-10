from pathlib import Path


def _get_project_base_dir() -> Path:
    start_dir = Path(".").resolve()
    current_dir = start_dir

    while True:
        marker_file_path = current_dir / "__topleveldir.txt"
        if marker_file_path.exists():
            return current_dir
        elif current_dir.parent == current_dir:
            raise Exception("Could not found OneForecast project base dir when searching down from: '{}'!".format(start_dir))
        else:
            current_dir = current_dir.parent

class DirectoryStructure:
    top_level_dir = _get_project_base_dir()

    project_dir = top_level_dir / 'approval_wip'

    TARGET_DIR = project_dir / 'target'
    LOCAL_EXPERIMENT_OUTPUT_DIR = project_dir / "local_output_dir"

    test_data_capture_dst_dir = project_dir / 'test_data_capture_dst_dir'
