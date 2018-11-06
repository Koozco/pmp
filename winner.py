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
import sys
import os

sys.path.append(os.path.join(".."))
from rules.borda import Borda
from preferences.profile import Profile
from preferences.preference import Preference

try:
    import numpy as np
    import ilp
except:
    # debug("No numeric libraries! Do not use ILP")
    pass

# TODO: fix it to work from console as before
#
# print winners
#


def print_winners(winners, candidates, data_out=None):
    for w in winners:
        print_or_save(w, candidates[w], data_out)


# returns list of candidates ids
def find_winners(config, preferences, data_out=None):
    C = config.get_candidates()
    m = len(C)
    k = config.get_k()
    rule = config.get_rule()

    candidates = range(m)
    preferences = [Preference(i) for i in preferences]

    profile = Profile(candidates, preferences)
    W = rule().find_committee(k, profile)

    print_winners(W, C, data_out)
    return W


if __name__ == "__main__":

    data_in = stdin
    data_out = stdout

    seed()

    k = 1

    R = Borda

    if len(argv) < 1 or (len(argv) >= 2 and argv[1].endswith("help")):
        print("This script computes election results\n")
        print("Invocation:")
        print("  python winner.py rule k <ordinal_election.out\n")
        print("Available rules:")
        # TODO: print available rules with description
        exit()

    if len(argv) >= 2:
        R = eval(argv[1])

    if len(argv) >= 3:
        k = int(argv[2])

    find_winners(R, k, data_in, data_out)
