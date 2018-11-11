import helpers
from helpers import Command
from os import system
from random import *
from sys import *

import pref2d2
from winner import find_winners_from_config
from visualize import *
from experiment_config import ExperimentConfig
from rules.borda import Borda

# TODO: add install_requires to setup.py?
# TODO clean imports
# TODO: separate experiment module
# TODO: test Impartial, non-2d
# TODO: what to do with preference? Where and how to create it? What for?
# TODO: think about files structure


image_import_fail = False
try:
    from PIL import Image
except ImportError:
    print("PIL module is not available. Pictures will not be generated.")
    image_import_fail = True


class Experiment:

    def __init__(self, conf=None):
        self.__config = conf
        if conf is None:
            self.__config = ExperimentConfig()
        self.__generated_dir_path = "generated"  # default directory path for generated files
        self.__k = 1
        self.__rule = Borda
        self.__filename = "default"
        self.__is_ordinal = True

    def init_from_input(self, commands, generated_dir_path):
        config = ExperimentConfig()
        self.__generated_dir_path = generated_dir_path

        command_line_id = 0
        while command_line_id < len(commands):
            command_line = commands[command_line_id]
            command = command_line[0]
            if command == "impartial":
                config.set_two_dimensional(False)
                config.impartial(int(command[1]), int(command[2]))
            elif command[0] == "#":
                pass
            elif command in ['voters', 'candidates']:
                distribution = commands[command_line_id + 1][0]
                args = commands[command_line_id + 1][1:]
                f = []
                # generate points
                if distribution == "circle":
                    f = lambda: helpers.generate_circle(float(args[0]), float(args[1]), float(args[2]), int(args[3]),
                                                        get_or_none(args, 4))
                elif distribution == "gauss":
                    f = lambda: helpers.generate_gauss(float(args[0]), float(args[1]), float(args[2]), int(args[3]),
                                                       get_or_none(args, 4))
                elif distribution == "uniform":
                    f = lambda: helpers.generate_uniform(float(args[0]), float(args[1]), float(args[2]), float(args[3]),
                                                         int(args[4]), get_or_none(args, 5))
                elif distribution == "image":
                    if image_import_fail:
                        return
                    f = lambda: helpers.generate_from_image(args[0], float(args[1]), float(args[2]), float(args[3]),
                                                            float(args[4]), int(args[5]), get_or_none(args, 6))
                if command == 'voters':
                    self.__config.add_command((Command.GEN_VOTERS, f))
                elif command == 'candidates':
                    self.__config.add_command((Command.GEN_CANDIDATES, f))
                command_line_id += 1
            else:
                # make a class object from string
                command_line[0] = eval(command_line[0])
                self.set_election(*command_line[:-1])
                self.__filename = command_line[-1]
            command_line_id += 1

    def set_generated_dir_path(self, dir_path):
        if not os.path.isabs(dir_path):
            dir_path = os.path.join(os.path.pardir, dir_path)
        self.__generated_dir_path = dir_path

    def get_generated_dir_path(self):
        return self.__generated_dir_path

    def set_election(self, rule, k):
        self.__rule = rule
        self.__k = int(k)

    def set_filename(self, name):
        self.__filename = name

    def get_k(self):
        return self.__k

    def get_rule(self):
        return self.__rule

    def run(self, visualization=False):
        dir_path = os.path.join(self.__generated_dir_path)

        if self.__config.is_two_dimensional():
            try:
                helpers.make_dirs(dir_path, exist_ok=True)
            except OSError:
                if not os.path.isdir(dir_path):
                    raise

        candidates, voters = self.__execute_commands()
        self.__run_election(candidates, voters, visualization)

    def __execute_commands(self):
        candidates = self.__config.get_candidates()
        voters = self.__config.get_voters()

        for experiment_command in self.__config.get_commands():
            command_type = experiment_command[0]
            args = experiment_command[1]
            if command_type == Command.GEN_CANDIDATES:
                candidates += experiment_command[1]()
            elif command_type == Command.GEN_VOTERS:
                voters += experiment_command[1]()
            elif command_type == Command.GEN_FROM_CANDIDATES:
                self.__is_ordinal = False
                voters += experiment_command[1](candidates)
            elif command_type == Command.IMPARTIAL:
                self.__is_ordinal = False
                candidates, voters = self.__impartial(*args)
        return candidates, voters

    # run election, compute winners
    # TODO: clean this part
    def __run_election(self, candidates, voters, visualization):
        output = self.__filename
        seed()
        if self.__is_ordinal:
            preferences = pref2d2.pref(candidates, voters)

            with open(os.path.join(self.__generated_dir_path, output + ".win"), "w") as data_out:
                winners = find_winners_from_config(self, candidates, preferences, data_out)

            print("WINNERS", winners)

            if self.__config.is_two_dimensional() and visualization:
                print("2D = True")
                if image_import_fail:
                    print("Cannot visualize results because of PIL import fail.")
                    return
                visualize(candidates, voters, winners, output, self.__generated_dir_path)
        else:
            print("NOT IMPLEMENTED")

    def __impartial(self, m, n):
        # preferences
        candidates = range(m)
        voters = []

        for p in range(n):
            x = range(m)
            shuffle(x)
            voters += [x]
        return candidates, voters


def get_or_none(l, n):
    try:
        return l[n]
    except:
        return "NONE"


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

    experiment = Experiment()
    experiment.init_from_input(cmd, generated_dir_path)
    experiment.run(visualization=True)
