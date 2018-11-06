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
    #  print C
    for v in voters:
        #    print v
        v_dist = compute_dist(v, candidates)
        v_sorted = sorted(v_dist, key=second)
        v_order = [cand for (cand, _) in v_sorted]
        #    print v_order
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


# read in the data in our format
# m n  (number of candidates and voters)
# x  y (m candidates in m lines)
# ...
# x  y (n voters in n lines)
# ...

# return (n,k,d,F,X)
def read_data(f):
    P = []
    C = []
    lines = f.readlines()
    (m, n) = lines[0].split()
    m = int(m)
    n = int(n)

    for l in lines[1:m + 1]:
        (x, y, p) = l.split()
        C += [(float(x), float(y), p)]

    for l in lines[m + 1:m + n + 1]:
        (x, y, ignored) = l.split()
        P += [(float(x), float(y))]

    return (m, n, C, P)


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

    (m, n, C, V) = read_data(data_in)

    P = preference_orders(C, V)
    printPrefOrders(C, V, P)
