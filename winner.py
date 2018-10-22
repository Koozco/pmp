################################
# winner.py -- Winner Computation
#
from doctest import debug
from random import *
from sys import *
from helpers import *
from itertools import *
from math import *
from copy import copy
from random import choice
# from sets import Set # TODO: check where is it used?
import sys
import os

# from core import *

# from rule_pr import *

sys.path.append(os.path.join(".."))
from rules.borda import Borda
from preferences.profile import Profile
from preferences.preference import Preference

# import rule packages
# for file in os.listdir("."):
#     if file.startswith("rule_") and file.endswith(".py"):
#         debug("RULES: %s" % file[:-3])
#         exec("from %s import *" % (file[:-3]))
#
# # irrespectively, import core rule packages
# from rule_weakly_separable import *
# from rule_proportional import *

try:
    import numpy as np
    import ilp
except:
    # debug("No numeric libraries! Do not use ILP")
    pass


# read in the data in our format
# m n  (number of candidates and voters)
# m candidate names
# ...
# pref1  (n preference orders)
# ...


# return (m,n,V)
def readData(f, k, data_out=None):
    V = []
    C = []
    lines = f.readlines()
    (m, n) = lines[0].split()
    m = int(m)
    n = int(n)

    print_or_save("{} {} {}".format(m, n, k), data_out)

    for l in lines[1:m + 1]:
        s = l.rstrip()
        C += [s]
        print_or_save(s, data_out)

    for l in lines[m + 1:m + n + 1]:
        print_or_save(l.rstrip(), data_out)
        s = l.split()[0:m]
        s = [int(x) for x in s]
        V += [s]

    return (m, n, C, V)


#
# print winners
#

def printWinners(W, C, k, data_out=None):
    for i in W:
        print_or_save(C[i], data_out)


def find_winners(R, k, data_in, data_out=None):
    (m, n, C, V) = readData(data_in, k, data_out)

    candidates = range(m)
    preferences = [Preference(i) for i in V]

    profile = Profile(candidates, preferences)
    W = R().find_committee(k, profile)

    printWinners(W, C, k, data_out)


def winner(name_in, output, rule, k_value, generated_dir_path):
    data_in = open(os.path.join(generated_dir_path, name_in), "r")
    data_out = open(os.path.join(generated_dir_path, output), "w")

    seed()

    k = 1
    R = Borda

    if rule is not None:
        R = eval(rule)  # TODO: replace this eval?

    if k_value is not None:
        k = int(k_value)

    find_winners(R, k, data_in, data_out)


if __name__ == "__main__":

    data_in = stdin
    data_out = stdout

    seed()

    k = 1

    R = Borda

    if len(argv) >= 2 and argv[1].endswith("help"):
        print("This script computes election results\n")
        print("Invocation:")
        print("  python winner.py rule k <ordinal_election.out\n")
        print("Available rules:")
        # for (rule, description) in RULES: # TODO: what is "RULES"?
        #     l = 10
        #     print("%s - %s" % (rule + " " * (l - len(rule)), description))
        exit()

    if len(argv) >= 2:
        R = eval(argv[1])

    if len(argv) >= 3:
        k = int(argv[2])

    find_winners(R, k, data_in, data_out)

