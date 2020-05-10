from itertools import takewhile
from pathlib import Path
from random import random, gauss, shuffle
from typing import List, Tuple

from PIL import Image

from aaa_pb.legacy.visualize import drawVisualization
from aaa_pb.legacy_adapters.winner_adapter import Winner_Adapter
from aaa_pb.model.ballot_calc import BallotCalc


class OldExperiment:

    @staticmethod
    def fromFile(input_file_path: Path,
                 output_dir_path: Path,
                 ballot_calc: BallotCalc) -> 'OldExperiment':
        with open(str(input_file_path), mode='r') as input_file:
            lines = input_file.readlines()
            commands_list = OldExperiment.__parseInputCommands(lines)

        return OldExperiment(commands=commands_list,
                             ballot_calc=ballot_calc,
                             output_dir_path=output_dir_path)

    @staticmethod
    def fromCommandList(commands: List[str],
                        output_dir_path: Path,
                        ballot_calc: BallotCalc) -> 'OldExperiment':

        return OldExperiment(commands=OldExperiment.__parseInputCommands(commands),
                             ballot_calc=ballot_calc,
                             output_dir_path=output_dir_path)

    def __init__(self, commands: List[str], ballot_calc: BallotCalc, output_dir_path: Path = Path(".")) -> None:
        # used for 2D
        self.C = []
        self.V = []

        # used for non-2D
        self.REAL_C = []
        self.REAL_V = []

        self.DATA = "C"
        self.GENERATED_DATA_FILE_NAME_PREFIX = "data"
        self.TWO_DIMENSIONAL = True

        # output dir
        self.OUTPUT_DIR_PATH = output_dir_path

        self.COMMANDS = commands
        self.ballot_calc = ballot_calc

    def run(self, rm_in_file: bool=False, rm_out_files: bool=False) -> None:
        # PBATKO TODO rm tmp files
        for command in self.COMMANDS:
            self.__executeCommand(command=command)

    def __createOutputFilePath(self, output_file_name: str) -> Path:
        return self.OUTPUT_DIR_PATH / output_file_name

    # GENERATE POINTS
    @staticmethod
    def __generateFromImage(filename, x1, y1, x2, y2, N, Party):
        img = Image.open(filename)
        rgb_im = img.convert('RGB')

        x, y = rgb_im.size
        density_map = []
        total_color_intensity = 0
        for i in range(x):
            for j in range(y):
                pixel = rgb_im.getpixel((i, j))
                color_intensity = (255 - pixel[0]) + (255 - pixel[1]) + (255 - pixel[2])
                coor1 = x1 + (float(i * (x2 - x1)) / x)
                coor2 = y2 - (float(j * (y2 - y1)) / y)
                density_map.append((coor1, coor2, color_intensity))
                total_color_intensity += color_intensity
        random_list = [random() * total_color_intensity for i in range(N)]
        result = []
        i = 0
        passed_intensity = 0
        for v in sorted(random_list):
            while passed_intensity < v:
                passed_intensity += density_map[i][2]
                i += 1
            result.append((density_map[i][0], density_map[i][1], Party))
        return result

    @staticmethod
    def __generateUniform(x1: float, y1: float, x2: float, y2: float, N: int, Party: str) -> List[Tuple[float, float]]:
        (x1, x2) = (min(x1, x2), max(x1, x2))
        (y1, y2) = (min(y1, y2), max(y1, y2))
        return [(random() * (x2 - x1) + x1, random() * (y2 - y1) + y1) for i in range(N)]

    @staticmethod
    def __generateGauss(x: float, y: float, sigma: float, N: int, Party: str) -> List[Tuple[float, float]]:
        return [(gauss(x, sigma), gauss(y, sigma)) for i in range(N)]

    @staticmethod
    def __generateCircle(x: float, y: float, r: float, N: int, Party: str) -> List[Tuple[float, float]]:
        count = 0
        L = []
        while (count < N):
            (px, py) = (random() * (2 * r) - r, random() * (2 * r) - r)
            if (px ** 2 + py ** 2 <= r ** 2):
                L += [(px + x, py + y)]
                count += 1
        return L

    # save data

    def __saveGeneratedData(self, output_file_name_prefix: str) -> None:

        if (self.TWO_DIMENSIONAL):
            output_file_path = self.__createOutputFilePath(output_file_name_prefix + ".in")
            # Cannot use .open() because returns a TextIOWrapper
            # https://docs.python.org/2/library/io.html#io.TextIOWrapper
            # output_file = output_file_path.open(mode="w")
            output_file = open(str(output_file_path), "w")

            m = len(self.C)
            n = len(self.V)
            print >> output_file, m, n
            for p in self.C:
                x = p[0]
                y = p[1]
                aWord = p[2]
                print >> output_file, x, y, aWord
            for p in self.V:
                x = p[0]
                y = p[1]
                aWord = p[2]
                print >> output_file, x, y, aWord

            output_file.close()

            the_2d2pref_output_file_path = self.__createOutputFilePath(output_file_name_prefix + ".out")

            self.ballot_calc.calculateFrom2PointsFile(output_file_path, the_2d2pref_output_file_path)

            # cmd = "python 2d2pref.py <{0} >{1}".format(output_file_path, the_2d2pref_output_file_path)
            # system(cmd)

        else:
            # TODO PBATKO haven't checked if this work after refactor
            output_file = open(output_file_name_prefix + ".out", "w")
            print >> output_file, len(self.REAL_C), len(self.REAL_V)
            for c in self.REAL_C:
                print >> output_file, c
            for v in self.REAL_V:
                s = ""
                for z in v:
                    s += str(z) + " "
                print >> output_file, s
            output_file.close()

    def impartial(self, M: int, N: int) -> None:
        self.REAL_C = range(M)

        for p in range(N):
            x = range(M)
            shuffle(x)
            self.REAL_V += [x]

    # compute winners

    def __computeWinners(self, rule_name: str, k: int, output_file_name_prefix: str) -> None:
        generated_data_file_path = self.__createOutputFilePath(self.GENERATED_DATA_FILE_NAME_PREFIX + ".out")
        winner_output_file_path = self.__createOutputFilePath(output_file_name_prefix + ".win")

        # old way of calling separate process (in a subshell)
        # cmd = "python winner.py {0} {1} {2} {3}".format(generated_data_file_path, output_file_path, rule, k)
        # print "Calling: '{0}'".format(cmd)
        # system(cmd)

        # TODO pass pathlib.Path object, not strings
        Winner_Adapter().calculateWinner(str(generated_data_file_path), str(winner_output_file_path), rule_name, k)

        if self.TWO_DIMENSIONAL:
            print("2D = {0}".format(self.TWO_DIMENSIONAL))
            img_file_output_path = self.OUTPUT_DIR_PATH / (output_file_name_prefix + ".png")

            drawVisualization(
                img_file_output_path=img_file_output_path,
                input_file_path=winner_output_file_path,
                rule_name=rule_name + "_" + str(k))
            # cmd = "python visualize.py {0} {1}".format(output_file_path, self.OUTPUT_DIR_PATH)
            # system(cmd)

    @classmethod
    def __getOrNoneString(cls, l: List[str], n: int) -> str:
        try:
            return l[n]
        except:
            return "NONE"

    # COMMAND EXECUTION

    def __executeCommand(self, command: List[str]) -> None:
        # print "Executing command: '{0}'".format(command)

        command_name = command[0]

        if command_name == "candidates":
            self.DATA = "self.C"
        elif command_name == "voters":
            self.DATA = "self.V"
        elif command_name == "circle":

            x = float(command[1])
            y = float(command[2])
            r = float(command[3])
            N = int(command[4])
            Party = self.__getOrNoneString(command, 5)

            P = self.__generateCircle(x, y, r, N, Party)
            X = eval(self.DATA)
            X += P

        elif command_name == "gauss":
            x = float(command[1])
            y = float(command[2])
            sigma = float(command[3])
            N = int(command[4])
            Party = self.__getOrNoneString(command, 5)

            P = self.__generateGauss(x, y, sigma, N, Party)
            X = eval(self.DATA)
            X += P

        elif command_name == "uniform":
            x1 = float(command[1])
            y1 = float(command[2])
            x2 = float(command[3])
            y2 = float(command[4])
            N = int(command[5])
            Party = self.__getOrNoneString(command, 6)

            P = self.__generateUniform(x1, y1, x2, y2, N, Party)
            X = eval(self.DATA)
            X += P

        elif command_name == "image":
            P = self.__generateFromImage(command[1], float(command[2]), float(command[3]), float(command[4]),
                                         float(command[5]),
                                         int(command[6]), self.__getOrNoneString(command, 7))
            X = eval(self.DATA)
            X += P
        elif (command_name == "generate"):
            self.GENERATED_DATA_FILE_NAME_PREFIX = command[1]
            self.__saveGeneratedData(self.GENERATED_DATA_FILE_NAME_PREFIX)

        elif (command_name == "impartial"):
            self.TWO_DIMENSIONAL = False
            self.impartial(int(command[1]), int(command[2]))

        else:
            voting_rule_name = command_name
            committee_size = int(command[1])
            output_file_name = command[2]
            self.__computeWinners(voting_rule_name, committee_size, output_file_name)

    # READ DATA IN
    @classmethod
    def __parseInputCommands(cls, lines: List[str]) -> List[List[str]]:
        parsedCommands = []

        for line in lines:
            parsedCommands += cls.__parseSingleCommand(command_str=line)

        return parsedCommands

    @classmethod
    def __parseSingleCommand(cls, command_str):
        # splits on any number of blank characters
        raw_words = command_str.split()
        # drop trailing comment starting with '#'
        words = list(takewhile(lambda x: x.lstrip()[0] != '#', raw_words))
        if len(words) > 0:
            return [words]
        else:
            return []

# MAIN
# if __name__ == "__main__":
#
#     if (len(argv) != 3):
#         print "ERROR: Expected exactly 2 arguments, got {0}".format(len(argv))
#         print "This scripts runs a single experiment (generates an elections, "
#         print "computes the results according to specified rules, and prepares visualizations)"
#         print
#         print "Invocation:"
#         print "  python experiment.py <description-file> <output-dir-path>"
#         exit(1)
#
#     input_file_arg = argv[1]
#     output_dir_arg = argv[2]
#
#     input_file_path = Path(input_file_arg)
#     output_dir_path = Path(output_dir_arg)
#
#     if not input_file_path.exists():
#         print "Input file '{0}' doesn't exist!".format(input_file_arg)
#         exit(1)
#
#     if not input_file_path.is_file():
#         print "Input file '{0}' is not a regular file!".format(input_file_arg)
#         exit(1)
#
#     if not output_dir_path.exists():
#         print "Output dir '{0}' doesn't exist!".format(output_dir_arg)
#         exit(1)
#
#     if not output_dir_path.is_dir():
#         print "Output dir '{0}' is not a directory!".format(output_dir_arg)
#         exit(1)
#
#     seed()
#
#     experiment = Experiment.fromFile(input_file_path, output_dir_path, ballot_calc=OrdinalBallotCalc)
#
#     experiment.run()
