################################
# winner.py -- Winner Computation
#
from random import seed
from sys import argv
from typing import List, Tuple, Any, Type

from aaa_pb.test_utils.record_elections_data_for_tests import RecordElectionsDataForTests
from aaa_pb.legacy.core import RULES
from aaa_pb.legacy.core import debug


class Winner_Adapter:
    # read in the data in our format
    # m n  (number of candidates and voters)
    # m candidate names
    # ...
    # pref1  (n preference orders)
    # ...
    # return (m,n,C,V)
    def readData(self, lines: List[str], k: int) -> Tuple[int ,int, List[str], List[List[int]]]:
        V = []
        C = []

        (m, n) = lines[0].split()
        m = int(m)
        n = int(n)

        for l in lines[1:m + 1]:
            s = l.rstrip()
            C += [s]

        for l in lines[m + 1:m + n + 1]:
            # skip first two numbers: they are 2d coordinates, TODO: do it in other places as well!
            s = l.split()[2:m + 2]
            s = [int(x) for x in s]
            V += [s]

        return (m, n, C, V)


    def writeHeader(self, input_file_lines: List[str], output_file: Any, k: int) -> None:
        lines = input_file_lines

        (m, n) = lines[0].split()
        m = int(m)  # no of candidates
        n = int(n)  # no of voters
        output_file.write("{0} {1} {2}\n".format(m, n, k))

        candidates_lines = lines[1:m + 1]
        for l in candidates_lines:
            output_file.write(l.rstrip() + "\n")

        voters_lines = lines[m + 1:m + n + 1]
        for l in voters_lines:
            output_file.write(l.rstrip() + "\n")


    #
    # print winners
    #

    def writeWinners(self, W: List[int], C: List[str], output_file: Any) -> None:
        debug("printwinners")
        for i in W:
            output_file.write(C[i] + "\n")


    def calculateWinner(self, input_file_path_arg: str, output_file_path_arg: str, rule_class: Type[Any], k: int) -> None:
        input_lines = open(input_file_path_arg, 'r').readlines()
        (m, n, C, V) = self.readData(input_lines, k)
        number_of_candidates = len(C)

        W = self.calculateWinnerSane(V, number_of_candidates, k, rule_class)

        output_file = open(output_file_path_arg, 'w')
        self.writeHeader(input_lines, output_file, k)
        self.writeWinners(W, C, output_file)

    def calculateWinnerSane(self, V, number_of_candidates, k, rule_class):
        # make a copy just in case
        V = [list(vote) for vote in V]

        RecordElectionsDataForTests.TEST_UTIL_HOOK.apply(
            V=V,
            k=k,
            number_of_candidates=number_of_candidates
        )

        W = rule_class.apply(V, number_of_candidates, k)
        print(W)
        if len(set(W)) != k:
            print("ERROR:")
            print("k: " + str(k))
            print("len(set(W)): " + str(len(set(W))))
            print("len(W): " + str(len(W)))
            print("rule_class: " + str(rule_class))
            print("")
            print("")
            print("")
            raise Exception
        # assert len(set(W)) == k  # sanity check

        return W

def main():
    k: int
    # TODO restore ability to use stdin and stdout
    # data_in = stdin
    # data_out = stdout
    seed()
    if len(argv) < 3:
        print("ERROR: Required at least to arguments: input and output files")
        exit(1)
    if argv[1] == "help":
        print("This script computes election results")
        print()
        print("Invocation:")
        print("  python winner.py rule k <ordinal_election.out")
        print()
        print("Available rules:")
        for (rule, description) in RULES:
            l = 10
            print("%s - %s" % (rule + " " * (l - len(rule)), description))
        exit()
    input_file_path_arg = argv[1]
    output_file_path_arg = argv[2]
    if len(argv) >= 4:
        rule_function_name = argv[3]
    else:
        rule_function_name = "kborda"
    if len(argv) == 5:
        committee_size_str = argv[4]
        k = int(committee_size_str)
    else:
        k = 1
    Winner_Adapter().calculateWinner(input_file_path_arg, output_file_path_arg, rule_function_name, k)


if __name__ == "__main__":
    main()
