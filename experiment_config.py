import helpers
import inspect
import os
import pref2d2
from random import *
from winner import find_winners_from_config
from visualize import *
from rules.borda import Borda
from enum import Enum

image_import_fail = False
try:
    from PIL import Image
except ImportError:
    print("PIL module is not available. Pictures will not be generated.")
    image_import_fail = True

# TODO: test Impartial, non-2d
# TODO: think about files structure
# TODO: how should Impartial work when it comes to Profiles and distance?


class Command(Enum):
    GEN_CANDIDATES = 1
    GEN_VOTERS = 2
    RUN_ELECTION = 3
    IMPARTIAL = 4


class ExperimentConfig:
    def __init__(self):
        self.__k = 1
        self.__rule = Borda
        self.__candidates = []
        self.__voters = []
        self.__commands = []
        self.__two_dimensional = True
        self.__generated_dir_path = "generated"  # default directory path for generated files

    def init_from_input(self, commands):
        command_line_id = 0
        while command_line_id < len(commands):
            command_line = commands[command_line_id]
            command = command_line[0]
            if command == "impartial":
                self.__two_dimensional = False
                self.impartial(int(command[1]), int(command[2]))
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
                    self.__commands.append((Command.GEN_VOTERS, f))
                elif command == 'candidates':
                    self.set_candidates((Command.GEN_CANDIDATES, f))
                command_line_id += 1
            else:
                # make a class object from string
                command_line[0] = eval(command_line[0])
                self.run_election(*command_line)
            command_line_id += 1

    def get_k(self):
        return self.__k

    def set_k(self, k):
        self.__k = k

    def get_rule(self):
        return self.__rule

    def set_rule(self, rule):
        self.__rule = rule

    def set_generated_dir_path(self, dir_path):
        if not os.path.isabs(dir_path):
            dir_path = os.path.join(os.path.pardir, dir_path)
        self.__generated_dir_path = dir_path

    def get_generated_dir_path(self):
        return self.__generated_dir_path

    def get_candidates(self):
        return self.__candidates

    def set_candidates(self, list_of_candidates):
        self.__candidates = list_of_candidates

    def add_candidates(self, list_of_candidates):
        if inspect.isfunction(list_of_candidates):
            self.__commands.append((Command.GEN_CANDIDATES, list_of_candidates))
        else:
            self.__candidates += list_of_candidates

    def add_one_candidate(self, position, party='None'):
        self.__candidates += [position + (party,)]

    def set_voters(self, list_of_voters):
        self.__voters = list_of_voters

    def add_voters(self, list_of_voters):
        if inspect.isfunction(list_of_voters):
            self.__commands.append((Command.GEN_VOTERS, list_of_voters))
        else:
            self.__voters += list_of_voters

    def add_one_voter(self, position, party='None'):
        self.__voters += [position + (party,)]

    def get_voters(self):
        return self.__voters

    def get_commands(self):
        return self.__commands

    def is_two_dimensional(self):
        return self.__two_dimensional

    def run_election(self, rule, k, output_filename):
        self.__k = int(k)
        self.__rule = rule
        self.__output_filename = output_filename
        self.__commands.append((Command.RUN_ELECTION, (output_filename,)))

    def impartial(self, m, n):
        self.__commands.append((Command.IMPARTIAL, (m, n)))

    def run(self):
        dir_path = os.path.join(self.__generated_dir_path)
        if self.__two_dimensional:
            try:
                helpers.make_dirs(dir_path, exist_ok=True)
            except OSError:
                if not os.path.isdir(dir_path):
                    raise

        for experiment_command in self.__commands:
            {
                Command.GEN_CANDIDATES: lambda fun: self.add_candidates(fun()),
                Command.GEN_VOTERS: lambda fun: self.add_voters(fun()),
                Command.RUN_ELECTION: lambda x: self.__run_election(*x),
                Command.IMPARTIAL: lambda x: self.__impartial(*x)
            }[experiment_command[0]](experiment_command[1])

    def __impartial(self, m, n):
        self.set_candidates(range(m))

        for p in range(n):
            x = range(m)
            shuffle(x)
            self.add_voters([x])

    # run election, compute winners
    # TODO: clean this part
    def __run_election(self, output):
        seed()
        preferences = pref2d2.pref(self)

        with open(os.path.join(self.__generated_dir_path, output + ".win"), "w") as data_out:
            winners = find_winners_from_config(self, preferences, data_out)

        print(winners)

        if self.__two_dimensional:
            print("2D = " + str(self.__two_dimensional))
            if image_import_fail:
                print("Cannot visualize results because of PIL import fail.")
                return
            visualize(self, winners, output)


def get_or_none(l, n):
    try:
        return l[n]
    except:
        return "NONE"
