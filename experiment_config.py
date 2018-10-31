import helpers
import os
import pref2d2
from random import *
from winner import winner
from visualize import *

image_import_fail = False
try:
    from PIL import Image
except ImportError:
    print("PIL module is not available. Pictures will not be generated.")
    image_import_fail = True

# TODO: refactor
# TODO: test Impartial, non-2d
# TODO: what to do with save_data


class ExperimentConfig:
    def __init__(self):
        self.__candidates = []
        self.__candidates_generating = []
        self.__voters = []
        self.__voters_generating = []
        self.__commands = []
        self.__two_dimensional = True
        self.__generated_dir_path = "generated" # default directory name for generated files

    # TODO: change it so that it is not executed until called
    def init_from_cmd(self, commands):
        command_line_id = 0
        while command_line_id < len(commands):
            command_line = commands[command_line_id]
            command = command_line[0]
            if command == 'generate':
                self.save_data(command_line[1])
            elif command == "impartial":
                self.__two_dimensional = False
                self.impartial(int(command[1]), int(command[2]))
            elif command[0] == "#":
                pass
            elif command in ['voters', 'candidates']:
                distribution = commands[command_line_id + 1][0]
                args = commands[command_line_id + 1][1:]
                generated_points = []
                # generate points
                if distribution == "circle":
                    generated_points = helpers.generateCircle(float(args[0]), float(args[1]), float(args[2]),
                                                              int(args[3]), get_or_none(args, 4))
                elif distribution == "gauss":
                    generated_points = helpers.generateGauss(float(args[0]), float(args[1]), float(args[2]),
                                                             int(args[3]), get_or_none(args, 4))
                elif distribution == "uniform":
                    generated_points = helpers.generateUniform(float(args[0]), float(args[1]), float(args[2]),
                                                               float(args[3]), int(args[4]), get_or_none(args, 5))
                elif distribution == "image":
                    if image_import_fail:
                        return
                    generated_points = helpers.generateFromImage(args[0], float(args[1]), float(args[2]),
                                                                 float(args[3]), float(args[4]), int(args[5]),
                                                                 get_or_none(args, 6))
                # fill with generated points
                if command == 'voters':
                    self.add_voters(generated_points)
                elif command == 'candidates':
                    self.set_candidates(generated_points)
                command_line_id += 1
            else:
                self.compute_winners(*command_line)
            command_line_id += 1

    def set_generated_dir_path(self, path):
        self.__generated_dir_path = path

    def set_candidates(self, list_of_candidates):
        self.__candidates = list_of_candidates

    def add_candidates_function(self, generating_function):
        self.__candidates_generating += [generating_function]

    def add_candidates(self, list_of_candidates):
        self.__candidates += list_of_candidates

    def add_candidate(self, position, party='None'):
        self.__candidates += [position + (party,)]

    def set_voters(self, list_of_voters):
        self.__voters = list_of_voters

    def add_voters_function(self, generating_function):
        self.__voters_generating += [generating_function]

    def add_voters(self, list_of_voters):
        self.__voters += list_of_voters

    def add_voter(self, position, party='None'):
        self.__voters += [position + (party,)]

    def get_candidates(self):
        return self.__candidates

    def get_voters(self):
        return self.__voters

    def get_commands(self):
        return self.__commands

    def is_two_dimensional(self):
        return self.__two_dimensional

    def save_data(self, filename):
        self.__commands.append(('save', filename))

    def compute_winners(self, rule, k, output_filename):
        self.__commands.append(('compute_winners', (rule, k, output_filename)))

    def impartial(self, m, n):
        self.set_candidates(range(m))

        for p in range(n):
            x = range(m)
            shuffle(x)
            self.add_candidates([x])

    def run(self):

        self.__generate_candidates()
       # self.__generate_voters()

        for experiment_command in self.__commands:
            {
                'save': lambda x: self.__save_data(x),
                'compute_winners': lambda x: self.__compute_winners(*x)
            }[experiment_command[0]](experiment_command[1])

            # save data

    def __save_data(self, name):
        self.__name = name
        dir_path = os.path.join(self.__generated_dir_path)

        if self.__two_dimensional:
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

            pref2d2.pref(str(name + ".in"), str(name + ".out"), self.__generated_dir_path)

        else:
            try:
                os.makedirs(dir_path)
            except OSError:
                if not os.path.isdir(dir_path):
                    raise

            f = open(os.path.join(dir_path, name + ".out"), "w")
            f.write("{} {}".format(len(self.__candidates), len(self.__voters)))
            for c in self.__candidates:
                f.write(c)
            for v in self.__voters:
                s = ""
                for z in v:
                    s += str(z) + " "
                f.write(s)
            f.close()

    # compute winners

    def __compute_winners(self, rule, k, output):
        # system("python winner.py <%s.out >%s.win %s %d" % (NAME, output, rule, k))
        winner(self.__name + ".out", output + ".win", rule, k, self.__generated_dir_path)
        if self.__two_dimensional:
            print("2D = " + str(self.__two_dimensional))
            if image_import_fail:
                print("Cannot visualize results because of PIL import fail.")
                return
            visualize(output, self.__generated_dir_path)  # TODO: make it work from console as well
            # system("python visualize.py {}".format(output))  # to delete

    def __generate_candidates(self):
        for gen_command in self.__candidates_generating:
            self.add_candidates(gen_command())

    # TODO: maybe one list of commands with enum on which thing to generate
    def __generate_voters(self):
        for gen_command in self.__voters_generating:
            self.add_voters(gen_command())


def get_or_none(l, n):
    try:
        return l[n]
    except:
        return "NONE"
