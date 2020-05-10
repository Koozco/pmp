import subprocess
from distutils.cmd import Command
from pathlib import Path
from typing import List

from setuptools import find_packages
from setuptools import setup

version = "0.0.1-SNAPSHOT"  # when changing manually the version update also the setup.cfg file


def _get_project_base_dir() -> Path:
    start_dir = Path(".").resolve()
    current_dir = start_dir

    while True:
        marker_file_path = current_dir / "__topleveldir.txt"
        if marker_file_path.exists():
            return current_dir
        elif current_dir.parent == current_dir:
            raise Exception(
                "Could not found OneForecast project base dir when searching down from: '{}'!".format(start_dir))
        else:
            current_dir = current_dir.parent


class PyTestTask:
    # https://docs.pytest.org/en/latest/usage.html#specifying-tests-selecting-tests
    # pytest test_ala.py::TestClass::test_method

    def run(self, python_path: List[Path]) -> None:
        Path("target").mkdir(parents=False, exist_ok=True)

        extra_python_path_str = ":".join([str(x) for x in python_path])

        command = f'PYTHONPATH="{extra_python_path_str}:$PYTHONPATH" pytest tests_unit --rootdir .'
        print(command)

        completed_process = subprocess.run(command, shell=True)

        returncode = completed_process.returncode
        if returncode != 0:
            raise Exception(f"pytest failed with exit code {returncode}")


class PytestCommand(Command):  # type: ignore

    description = "Runs unit tests"
    user_options = []

    def initialize_options(self) -> None:
        pass

    def finalize_options(self) -> None:
        pass

    def run(self) -> None:
        project_dir = _get_project_base_dir() / 'mostly_ordinal'
        src_dirs = [
            project_dir / 'src',
            project_dir / 'tests_unit'
        ]
        PyTestTask().run(python_path=src_dirs)


if __name__ == "__main__":
    setup(
        name="MostlyOrdinal",
        version=version,
        packages=find_packages(where='src'),
        package_dir={'': 'src'},
        zip_safe=False,
        cmdclass={
            # "clean": None,
            # "yapf": None,
            # "mypy": None,
            # "lint": None,
            "unit_tests": PytestCommand
        },
    )
