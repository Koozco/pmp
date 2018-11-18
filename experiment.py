import os
from random import seed
from sys import *

try:
    from pmp.experiments.experiment import Experiment
    from pmp.experiments.experiment_config import ExperimentConfig
    from pmp.experiments import generating_functions
    from pmp.experiments.helpers import Command
    from pmp.rules import *
except (ImportError, NameError) as e:
    print("Cannot import pmp. Check whether pmp is installed.\n" + str(e))
    exit()

image_import_fail = False
try:
    from PIL import Image
except (ImportError, NameError):
    print("PIL module is not available. Pictures will not be generated.")
    image_import_fail = True


def init_from_input(commands, generated_dir_path):
    config = ExperimentConfig()
    experiment = Experiment(config)

    command_line_id = 0
    while command_line_id < len(commands):
        command_line = commands[command_line_id]
        command = command_line[0]
        if command == "impartial":
            experiment.two_dimensional = False
            config.impartial(int(command[1]), int(command[2]))
        elif command[0] == "#":
            pass
        elif command in ['voters', 'candidates']:
            distribution = commands[command_line_id + 1][0]
            args = commands[command_line_id + 1][1:]
            f = []
            # generate points
            if distribution == "circle":
                f = lambda: generating_functions.generate_circle(float(args[0]), float(args[1]), float(args[2]),
                                                                 int(args[3]), get_or_none(args, 4))
            elif distribution == "gauss":
                f = lambda: generating_functions.generate_gauss(float(args[0]), float(args[1]), float(args[2]),
                                                                int(args[3]), get_or_none(args, 4))
            elif distribution == "uniform":
                f = lambda: generating_functions.generate_uniform(float(args[0]), float(args[1]), float(args[2]),
                                                                  float(args[3]), int(args[4]),
                                                                  get_or_none(args, 5))
            elif distribution == "image":
                if image_import_fail:
                    return
                f = lambda: generating_functions.generate_from_image(args[0], float(args[1]), float(args[2]),
                                                                     float(args[3]), float(args[4]), int(args[5]),
                                                                     get_or_none(args, 6))
            if command == 'voters':
                config.add_command((Command.GEN_VOTERS, f))
            elif command == 'candidates':
                config.add_command((Command.GEN_CANDIDATES, f))
            command_line_id += 1
        else:
            # make a class object from string
            command_line[0] = eval(command_line[0])
            experiment.set_election(*command_line[:-1])
            filename = command_line[-1]
        command_line_id += 1
    experiment.set_generated_dir_path(generated_dir_path)
    experiment.set_filename(filename)
    return experiment


def get_or_none(l, n):
    try:
        return l[n]
    except (TypeError, IndexError):
        return 'None'


# READ DATA IN
def read_experiment_data(f):
    commands = []
    lines = f.readlines()

    for l in lines:
        s = l.split()
        if len(s) > 0:
            commands += [s]
    return commands

if __name__ == "__main__":
    args_number = len(argv)
    if (args_number == 1 and stdin.isatty()) or args_number > 2 or (args_number > 1 and argv[1] == "-help"):
        print("This scripts runs a single experiment (generates an elections, "
              "\ncomputes the results according to specified rules, and prepares visualizations)")
        print("\nInvocation:")
        print("  python experiment.py [path_to_output_directory] <description.input")
        exit()

    seed()
    data_in = stdin
    data_out = stdout
    generated_dir_path = "generated"
    if args_number > 1:
        generated_dir_path = argv[1]
        if not os.path.isabs(generated_dir_path):
            generated_dir_path = os.path.join(os.path.pardir, generated_dir_path)

    cmd = read_experiment_data(data_in)

    experiment = init_from_input(cmd, generated_dir_path)
    experiment.run(visualization=True, save_win=True)
