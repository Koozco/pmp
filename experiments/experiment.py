from random import seed, shuffle
from sys import *

from . import helpers
from . import generating_functions
from .experiment_config import ExperimentConfig
from .helpers import Command
from .visualize import *
from preferences.ordinal import Ordinal
from preferences.profile import Profile
from rules.borda import Borda
from saving_files import save_to_file

# TODO: test Impartial, non-2d
# TODO: think about files structure


image_import_fail = False
try:
    from PIL import Image
except (ImportError, NameError):
    print("PIL module is not available. Pictures will not be generated.")
    image_import_fail = True


class Experiment:
    def __init__(self, conf=None):
        self.__config = conf
        if conf is None:
            self.__config = ExperimentConfig()
        self.__generated_dir_path = "generated"  # default directory path for generated files
        self.k = 1
        self.rule = Borda
        self.filename = "default"
        self.is_ordinal = True

    def init_from_input(self, commands, generated_dir_path):
        config = ExperimentConfig()
        self.__generated_dir_path = generated_dir_path

        command_line_id = 0
        while command_line_id < len(commands):
            command_line = commands[command_line_id]
            command = command_line[0]
            if command == "impartial":
                config.two_dimensional = False
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
                    self.__config.add_command((Command.GEN_VOTERS, f))
                elif command == 'candidates':
                    self.__config.add_command((Command.GEN_CANDIDATES, f))
                command_line_id += 1
            else:
                # make a class object from string
                command_line[0] = eval(command_line[0])
                self.set_election(*command_line[:-1])
                self.filename = command_line[-1]
            command_line_id += 1

    def set_generated_dir_path(self, dir_path):
        if not os.path.isabs(dir_path):
            dir_path = os.path.join(os.path.pardir, dir_path)
        self.__generated_dir_path = dir_path

    def get_generated_dir_path(self):
        return self.__generated_dir_path

    def set_election(self, rule, k):
        self.rule = rule
        self.k = int(k)

    def set_filename(self, name):
        self.filename = name

    def run(self, visualization=False, n=1):
        dir_path = os.path.join(self.__generated_dir_path)

        try:
            helpers.make_dirs(dir_path, exist_ok=True)
        except OSError:
            if not os.path.isdir(dir_path):
                raise

        for _ in range(n):
            candidates, voters, preferences = self.__execute_commands()
            if self.is_ordinal:
                winners = self.__run_election(candidates, preferences)
            else:
                winners = self.__run_election(candidates, preferences)

            save_to_file(candidates, preferences, voters, self.k, winners)

            if visualization:
                self.__visualize(candidates, voters, winners)

    def __execute_commands(self):
        candidates = self.__config.get_candidates()
        voters = self.__config.get_voters()
        preferences = []

        for experiment_command in self.__config.get_commands():
            command_type = experiment_command[0]
            args = experiment_command[1]
            if command_type == Command.GEN_CANDIDATES:
                candidates += experiment_command[1]()
            elif command_type == Command.GEN_VOTERS:
                voters += experiment_command[1]()
            elif command_type == Command.GEN_FROM_CANDIDATES:
                self.is_ordinal = False
                voters, preferences = experiment_command[1](candidates)
            elif command_type == Command.IMPARTIAL:
                self.is_ordinal = False
                candidates, preferences = impartial(*args)
        if not preferences:
            preferences = preference_orders(candidates, voters)
        return candidates, voters, preferences

    # run election, compute winners
    def __run_election(self, candidates, preferences):
        seed()

        profile = Profile(candidates, preferences)
        if self.k > len(candidates):
            print("k is too big. Not enough candidates to find k winners.")
            return

        return self.rule().find_committee(self.k, profile)

    def __visualize(self, candidates, voters, winners):
        if self.__config.two_dimensional:
            if image_import_fail:
                print("Cannot visualize results because of PIL import fail.")
                return

            if not self.is_ordinal:
                print("Cannot visualize preferences that are not ordinal.")
                return

            visualize(candidates, voters, winners, self.filename, self.__generated_dir_path)
        else:
            print("Cannot visualize non 2D.")


def impartial(m, n):
    # preferences
    candidates = list(range(m))
    voters = []

    for p in range(n):
        x = list(range(m))
        shuffle(x)
        voters += [x]
    preferences = [Ordinal(voter) for voter in voters]
    return candidates, preferences


# Compute the distances of voter v from the candidates in set C
# outputs a list of the format (i,d) where i is the candidate
# name and d is the distance
#
def compute_dist(v, candidates):
    m = len(candidates)
    d = [(j, dist(v, candidates[j])) for j in range(m)]
    return d


def preference_orders(candidates, voters):
    preferences = []

    for v in voters:
        v_dist = compute_dist(v, candidates)
        v_sorted = sorted(v_dist, key=lambda x: x[1])
        v_order = [candidate_id for (candidate_id, _) in v_sorted]
        preferences += [Ordinal(v_order)]
    return preferences


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

    experiment = Experiment()
    experiment.init_from_input(cmd, generated_dir_path)
    experiment.run(visualization=True)
