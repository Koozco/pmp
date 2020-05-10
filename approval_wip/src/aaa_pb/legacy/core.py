import sys
from math import *

# directory of rules (each entry is (fucntion_name, description)
# when implementig a rule, precede the function by adding an
# entry to the RULES list
RULES = []

debug_on = True


def debug(s):
    if (debug_on):
        print(s, file=sys.stderr)


def negsecond(x):
    return -x[1]


eps = 0.00001  # max error allowed


def lambertw(x):  # Lambert W function using Newton's method
    w = x
    while True:
        ew = exp(w)
        wNew = w - (w * ew - x) / (w * ew + ew)
        if abs(w - wNew) <= eps: break
        w = wNew
    return w
