import helpers
from random import *

image_import_fail = False
try:
    from PIL import Image
except ImportError:
    print("PIL module is not available. Pictures will not be generated.")
    image_import_fail = True

# TODO: refactor
# TODO: Impartial, non-2d


class ExperimentConfig:
    def __init__(self):
        self.__candidates = []
        self.__voters = []
        self.__commands = []
        self.__two_dimensional = True
        # generated_dir_path # default directory name for generated files

    def init_from_cmd(self, commands):
        command_line_id = 0
        while command_line_id < len(commands):
            command_line = commands[command_line_id]
            command = command_line[0]
            if command == 'generate':
                self.save_data(command_line[1])
            elif command == "impartial":
                self.__two_dimensional = False
                impartial(int(command[1]), int(command[2]))
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
                    self.set_voters(generated_points)
                elif command == 'candidates':
                    self.set_candidates(generated_points)
                command_line_id += 1
            else:
                self.compute_winners(*command_line)
            command_line_id += 1

    def set_candidates(self, list_of_candidates):
        self.__candidates = list_of_candidates

    def set_voters(self, list_of_voters):
        self.__voters = list_of_voters

    def get_candidates(self):
        return self.__candidates

    def get_voters(self):
        return self.__voters

    def get_commands(self):
        return self.__commands

    def save_data(self, filename):
        self.__commands.append(('save', filename))

    def compute_winners(self, rule, k, output_filename):
        self.__commands.append(('compute_winners', (rule, k, output_filename)))


def get_or_none(l, n):
    try:
        return l[n]
    except:
        return "NONE"


def impartial(M, N):
    global REAL_C
    global REAL_V

    REAL_C = range(M)

    for p in range(N):
        x = range(M)
        shuffle(x)
        REAL_V += [x]
