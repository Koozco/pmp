################################
# 2d2pref --- converts 2D points to preference orders
#

from sys import *
import os
from itertools import *


#############################################################
#
# functions for preparing the preference profile


def dist(x, y):
    return (sum([(x[i] - y[i]) ** 2 for i in range(len(x))])) ** 0.5


# Compute the distances of voter v from the candidates in set C
# outputs a list of the format (i,d) where i is the candidate
# name and d is the distance
#
def computeDist(v, C):
    m = len(C)
    d = [(j, dist(v, C[j])) for j in range(m)]
    return d


def second(x):
    return x[1]


def preferenceOrders(C, V):
    P = []
    #  print C
    for v in V:
        #    print v
        v_dist = computeDist(v, C)
        v_sorted = sorted(v_dist, key=second)
        #    print v_sorted
        v_order = [cand for (cand, dis) in v_sorted]
        #    print v_order
        P += [v_order]
    return P


# Print pref orders
# m n (number of candidates and voters)
# m lines with candidate names (number position)
# n lines with preference orders (followed by positions)

# TODO: move to helpers or sth? used in other class
def print_or_save(value, data_out=None):
    if data_out is None:
        print(value)
    else:
        data_out.write(value + '\n')

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
def readData(f):
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


def pref(in_name, out_name):
    # TODO: check existence
    # data_in = open(os.path.join("..", "in", in_name))
    # data_out = open(os.path.join("..", "out", out_name))

    data_in = open(in_name, "r")
    data_out = open(out_name, "w")
    (m, n, C, V) = readData(data_in)

    P = preferenceOrders(C, V)
    printPrefOrders(C, V, P, data_out)

# MAIN



if __name__ == "__main__":

    if len(argv) > 1:
        print("This script converts an election in the 2D Euclidean format to a preference-order based one\n")
        print("Invocation:")
        print("  python pref2d2.py  <2d_point.in >election.out")
        exit()

    data_in = stdin
    data_out = stdout

    (m, n, C, V) = readData(data_in)

    P = preferenceOrders(C, V)
    printPrefOrders(C, V, P)
