import helpers
from os import system
from random import *
from sys import *
from visualize import *
from experiment_config import ExperimentConfig

# TODO: add install_requires to setup.py?
# TODO clean imports
# TODO: separate experiment module

# TODO: make it a class to run multiple experiments ?

image_import_fail = False
try:
    from PIL import Image
except ImportError:
    print("PIL module is not available. Pictures will not be generated.")
    image_import_fail = True


class Experiment:

    def __init__(self, conf):
        self.__config = conf


# READ DATA IN
def read_data(f):
    commands = []
    lines = f.readlines()

    for l in lines:
        s = l.split()
        if len(s) > 0:
            commands += [s]
    return commands


# MAIN

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

    cmd = read_data(data_in)

    config = ExperimentConfig()
    config.set_generated_dir_path(generated_dir_path)
    config.init_from_input(cmd)
    config.run()
