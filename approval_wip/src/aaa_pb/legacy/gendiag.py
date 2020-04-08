from sys import *

from pathlib import Path

from aaa_pb.legacy.old_experiment import OldExperiment
import new_experiment





def runSeriesOfExperiments(election_instance,
                           output_dir_path,
                           rule_name,
                           committee_size,
                           election_from,
                           election_to,
                           ballot_calc):
    # type: (new_experiment.ElectionInstance, Path, str, int, int, int) -> None

    for i in range(election_from, election_to + 1):
        election_data_name = "data_{0}_{1}_{2}".format(rule_name, committee_size, i)


        command_list = createCommandsList(committee_size, election_data_name, i, rule_name, template)

        experiment = OldExperiment.fromCommandList(
            commands=command_list,
            output_dir_path=output_dir_path,
            ballot_calc=ballot_calc)

        experiment.run()

    pass

def createCommandsList(committee_size, i, rule_name):
    election_results_name = "{0}_{1}-{2}".format(rule_name, committee_size, i)
    commands_list = ["{0} {1} {2}".format(rule_name, committee_size, election_results_name)]
    return commands_list


# MAIN
# if __name__ == "__main__":
#
#     if (len(argv) != 7):
#         print "Invocation:"
#         print "  python gendiag.py  input_template rule #from #to #committee_size"
#         exit()
#
#     # get arguments
#     output_dir_arg = argv[1]
#     input_template_file_path_arg = argv[2]
#
#     output_dir_path = Path(output_dir_arg)
#     input_template_file_path = Path(input_template_file_path_arg)
#
#     if not output_dir_path.exists():
#         print "Output dir '{0}' doesn't exist!".format(output_dir_arg)
#         exit(1)
#
#     if not output_dir_path.is_dir():
#         print "Output dir '{0}' is not a directory!".format(output_dir_arg)
#         exit(1)
#
#     if not input_template_file_path.exists():
#         print "Input file '{0}' doesn't exist!".format(input_template_file_path_arg)
#         exit(1)
#
#     if not input_template_file_path.is_file():
#         print "Input file '{0}' is not a regular file!".format(input_template_file_path_arg)
#         exit(1)
#
#     rule_name = argv[3]
#     election_from = int(argv[4])
#     election_to = int(argv[5])
#     committee_size = int(argv[6])
#
#     runSeriesOfExperiments(input_template_file_path, output_dir_path, rule_name, committee_size, election_from,
#                            election_to)
