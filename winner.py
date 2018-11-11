################################
# winner.py -- Winner Computation
#
from doctest import debug
from random import *
from sys import *

from helpers import *
from itertools import *
from math import *
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

#
# print winners
#


def print_winners(winners, cands, data_out=None):
    for w in winners:
        print_or_save(w, cands[w], data_out)


# returns list of candidates ids
def find_winners_from_config(experiment, candidates, preferences, data_out=None):
    k = experiment.get_k()
    rule = experiment.get_rule()
    return find_winners(rule, k, candidates, preferences, data_out)


# returns list of candidates ids
def find_winners(rule, k, candidates, preferences, data_out=None):
    candidates_ids = range(len(candidates))
    preferences = [Preference(i) for i in preferences]

    profile = Profile(candidates_ids, preferences)
    winners = rule().find_committee(k, profile)
    print_winners(winners, candidates, data_out)
    return winners


if __name__ == "__main__":

    data_in = stdin

    seed()
    # default values
    rule = Borda
    k = 1

    if len(argv) < 1 or (len(argv) >= 2 and argv[1].endswith("help")):
        print("This script computes election results\n")
        print("Invocation:")
        print("  python winner.py rule k <ordinal_election.out\n")
        print("Available rules:")
        # TODO: print available rules with description
        exit()

    if len(argv) >= 2:
        rule = eval(argv[1])

    if len(argv) >= 3:
        k = int(argv[2])

    candidates, _, preferences = read_data(data_in)
    find_winners(rule, k, candidates, preferences)
