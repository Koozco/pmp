################################
# 2d2pref --- converts 2D points to preference orders
#

from sys import *
import os
from helpers import *
from itertools import *


#############################################################
#
# functions for preparing the preference profile

# TODO: make it work both ways

def dist(x, y):
    if type(x) is not tuple:
        return (x - y) ** 2
    length = len(x)
    if isinstance(x[-1], str):
        length -= 1
    return sum([(x[i] - y[i]) ** 2 for i in range(length)]) ** 0.5


# Compute the distances of voter v from the candidates in set C
# outputs a list of the format (i,d) where i is the candidate
# name and d is the distance
#
def compute_dist(v, candidates):
    m = len(candidates)
    d = [(j, dist(v, candidates[j])) for j in range(m)]
    return d


def second(x):
    return x[1]


def preference_orders(candidates, voters):
    preferences = []

    for v in voters:
        v_dist = compute_dist(v, candidates)
        v_sorted = sorted(v_dist, key=second)
        v_order = [cand for (cand, _) in v_sorted]
        preferences += [v_order]
    return preferences


# Print pref orders
# m n (number of candidates and voters)
# m lines with candidate names (number position)
# n lines with preference orders (followed by positions)

def printPrefOrders(C, V, P, data_out=None):
    m = len(C)
    n = len(V)
    print_or_save("{} {}".format(m, n), data_out)

    for i in range(len(C)):
        print_or_save("{} {} {} {}".format(i, C[i][0], C[i][1], C[i][2]), data_out)

    for i in range(len(P)):
        print_or_save("{} {} {}".format(" ".join([str(p) for p in P[i]]), V[i][0], V[i][1]), data_out)


def pref(config):
    candidates = config.get_candidates()
    voters = config.get_voters()

    preferences = preference_orders(candidates, voters)
    # printPrefOrders(C, V, P, data_out)
    return preferences
#
# MAIN


# TODO: add path to generated directory
if __name__ == "__main__":

    if len(argv) > 1:
        print("This script converts an election in the 2D Euclidean format to a preference-order based one\n")
        print("Invocation:")
        print("  python pref2d2.py <2d_point.in >election.out")
        exit()

    data_in = stdin
    data_out = stdout

    C, V, P = read_data(data_in)

    printPrefOrders(C, V, P)
