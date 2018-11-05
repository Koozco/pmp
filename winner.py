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


#
# print winners
#

def printWinners(W, C, k, data_out=None):
    for i in W:
        print_or_save(i, C[i], data_out)


# returns list of candidates ids
def find_winners(config, P, data_out=None):
    C = config.get_candidates()
    V = P
    m = len(C)
    k = config.get_k()
    R = config.get_rule()

    candidates = range(m)
    preferences = [Preference(i) for i in V]

    profile = Profile(candidates, preferences)
    W = R().find_committee(k, profile)

    printWinners(W, C, k, data_out)
    return W

# not saving files and reading from them

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
        # for (rule, description) in RULES:
        #     l = 10
        #     print("%s - %s" % (rule + " " * (l - len(rule)), description))
        exit()

    if len(argv) >= 2:
        R = eval(argv[1])

    if len(argv) >= 3:
        k = int(argv[2])

    find_winners(R, k, data_in, data_out)

