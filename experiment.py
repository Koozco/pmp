import os
import helpers
from os import system
from random import *
from sys import *
from visualize import *
from winner import winner
from experiment_config import ExperimentConfig

# TODO: add install_requires to setup.py?
# TODO clean imports
# TODO: separate experiment module

image_import_fail = False
try:
    from PIL import Image
except ImportError:
    print("PIL module is not available. Pictures will not be generated.")
    image_import_fail = True


import pref2d2


class Experiment():

    def __init__(self, conf):
        self.__candidates = conf.get_candidates()
        self.__voters = conf.get_voters()
        self.__commands = conf.get_commands()
        self.__name = "data"

    def run(self):
        for experiment_command in self.__commands:
            {
                'save': lambda x: self.save_data(x),
                'compute_winners': lambda x: self.compute_winners(*x)
            }[experiment_command[0]](experiment_command[1])

    # save data
    def save_data(self, name):
        self.__name = name
        global TWO_DIMENSIONAL
        global REAL_C
        global REAL_V

        if TWO_DIMENSIONAL:
            dir_path = os.path.join(generated_dir_path)
            try:
                helpers.make_dirs(dir_path, exist_ok=True)
            except OSError:
                if not os.path.isdir(dir_path):
                    raise

            f = open(os.path.join(dir_path, name + ".in"), "w")
            m = len(self.__candidates)
            n = len(self.__voters)
            f.write("{} {}\n".format(m, n))
            for p in self.__candidates:
                f.write("{} {} {}\n".format(p[0], p[1], p[2]))
            for p in self.__voters:
                f.write("{} {} {}\n".format(p[0], p[1], p[2]))
            f.close()

            pref2d2.pref(str(name + ".in"), str(name + ".out"), generated_dir_path)
            # system("python pref2d2.py <%s.in >%s.out" % (name, name))

        else:
            dir_path = os.path.join(generated_dir_path)
            try:
                os.makedirs(dir_path)
            except OSError:
                if not os.path.isdir(dir_path):
                    raise

            f = open(os.path.join(dir_path, name + ".out"), "w")
            f.write("{} {}".format(len(REAL_C), len(REAL_V)))
            for c in REAL_C:
                f.write(c)
            for v in REAL_V:
                s = ""
                for z in v:
                    s += str(z) + " "
                f.write(s)
            f.close()

    # compute winners

    def compute_winners(self, rule, k, output):
        # system("python winner.py <%s.out >%s.win %s %d" % (NAME, output, rule, k))
        winner(self.__name + ".out", output + ".win", rule, k, generated_dir_path)
        if TWO_DIMENSIONAL:
            print("2D = " + str(TWO_DIMENSIONAL))
            if image_import_fail:
                print("Cannot visualize results because of PIL import fail.")
                return
            visualize(output, generated_dir_path)  # TODO: make it work from console as well
            # system("python visualize.py {}".format(output))  # to delete


# used for non-2D
REAL_C = []
REAL_V = []

TWO_DIMENSIONAL = True
generated_dir_path = "generated"


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
    if args_number > 2 or (args_number > 1 and argv[1] == "-help"):
        print("This scripts runs a single experiment (generates an elections, "
              "\ncomputes the results according to specified rules, and prepares visualizations)")
        print("\nInvocation:")
        print("  python experiment.py [path_to_output_directory]  <description.input")
        exit()

    seed()
    # TODO: store dir_path in config
    data_in = stdin
    data_out = stdout
    if args_number > 1:
        generated_dir_path = argv[1]
        if not os.path.isabs(generated_dir_path):
            generated_dir_path = os.path.join(os.path.pardir, generated_dir_path)

    cmd = read_data(data_in)

    config = ExperimentConfig()
    config.init_from_cmd(cmd)
    e = Experiment(config)
    e.run()
