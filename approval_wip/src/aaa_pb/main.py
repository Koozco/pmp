import sys

from aaa_pb.directory_structure import DirectoryStructure
from aaa_pb.runners.main_runner import MainRunner
from aaa_pb.utils.date_time_utils import DateTimeUtils

if __name__ == '__main__':
    data_time_str = DateTimeUtils.getDateTimeFileName()

    data_for_tests_dst_dir = DirectoryStructure.test_data_capture_dst_dir / f'ordinal-cv4_{data_time_str}'

    cli_args = sys.argv[1:]
    MainRunner.run_with_hardcoded_args(
        data_time_str=DateTimeUtils.getDateTimeFileName()
    )
    # MainRunner.run(argv=cli_args)
