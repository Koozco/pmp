import sys
from pathlib import Path
from sys import exit
from typing import List, Any

from aaa_pb.utils.path_validator import PathValidator


def readData(lines: List[str]) -> Any:

    (m, n, k) = lines[0].split()
    m = int(m)
    n = int(n)
    k = int(k)

    C = []
    V = []
    W = []

    for l in lines[1:m + 1]:
        s = l.split()[1:]
        s = [float(s[0]), float(s[1])]
        C += [s]

    for l in lines[m + 1:m + n + 1]:
        s = l.split()[m:]
        s = [float(x) for x in s]
        V += [s]

    for l in lines[n + m + 1:n + m + k + 1]:
        s = l.split()[1:]
        s = [float(s[0]), float(s[1])]
        #    s = [float(x) for x in s]
        W += [s]

    return (m, n, k, C, V, W)


class OldHistogram:

    def __init__(self, number_of_experiments, input_dir_path, rule_name_with_committee_size):
        self.X1 = -3
        self.X2 = 3
        self.Y1 = -3
        self.Y2 = 3
        self.PPU = 20  # points per unit

        self.W = (self.X2 - self.X1) * self.PPU
        self.H = (self.Y2 - self.Y1) * self.PPU

        self.HISTOGRAM = [[0] * self.W for i in range(self.H)]

        self.MAX = 0

        self.number_of_experiments = number_of_experiments
        self.input_dir_path = input_dir_path
        self.rule_name_with_committee_size = rule_name_with_committee_size

    def computeHistogram(self):
        for i in range(1, self.number_of_experiments + 1):
            print(i)

            input_file_path = self.input_dir_path / "{0}-{1}.win".format(self.rule_name_with_committee_size, i)

            with open(str(input_file_path), 'r') as win_file:

                try:
                    lines = win_file.readlines()
                    (m, n, k, C, V, Winner) = readData(lines)

                    self.computeHistogramIncrementallySane(Winner)
                except IOError:
                    print("No file", rule_name_with_committee_size + "-" + str(i))
                    exit(1)

    def computeHistogramIncrementallySane(self, Winner):
        for (x, y) in Winner:
            if x < self.X1 or x > self.X2 or y < self.Y1 or y > self.Y2:
                continue
            x -= self.X1
            y -= self.Y1
            x *= self.PPU
            y *= self.PPU
            self.HISTOGRAM[int(y)][int(x)] += 1

            if (self.HISTOGRAM[int(y)][int(x)] > self.MAX):
                self.MAX = self.HISTOGRAM[int(y)][int(x)]

    def calculateAndPrintMaxAndTotal(self):
        #  print count

        print("MAX = ", self.MAX)

        MAX = 0
        TOTAL = 0
        for y in range(self.H):
            for x in range(self.W):
                TOTAL += self.HISTOGRAM[y][x]
                if (self.HISTOGRAM[y][x] > MAX):
                    MAX = self.HISTOGRAM[y][x]

        print("WRITING")
        print("MAX = %d   TOTAL = %d" % (MAX, TOTAL))

    def writeHistFile(self, output_dir_path, output_file_name):
        path = output_dir_path / output_file_name
        self.writeHistFileSaner(path)

    def writeHistFileSaner(self, output_path: Path) -> None:
        lines = [
            "{0} {1}".format(self.W, self.H)
        ]

        for y in range(self.H):
            line_tmp = ""
            for x in range(self.W):
                line_tmp += "{0} ".format(self.HISTOGRAM[y][x])
            lines.append(line_tmp)

        output_path.write_text(data="\n".join(lines))





if __name__ == '__main__':
    argv = sys.argv

    if len(argv) != 5:
        print("Expected 4 arguments, actual: {0}!".format(len(argv)))
        exit(1)

    input_dir_path = PathValidator(argv[1], "Input dir") \
        .exists() \
        .is_dir() \
        .get_path()

    output_dir_path = PathValidator(argv[2], "Output dir") \
        .exists() \
        .is_dir() \
        .get_path()

    rule_name_with_committee_size = argv[3]
    number_of_experiments = int(argv[4])

    histogram = OldHistogram(number_of_experiments, input_dir_path, rule_name_with_committee_size)
    histogram.calculateAndPrintMaxAndTotal()
    histogram.computeHistogram()

    rule_name_with_committee_size = (rule_name_with_committee_size + ".hist")
    histogram.writeHistFile(
        output_dir_path=output_dir_path,
        output_file_name=rule_name_with_committee_size)
