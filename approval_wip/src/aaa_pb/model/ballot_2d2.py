################################
# 2d2pref --- converts 2D points to preference orders
#

import random
from typing import Dict, List

from pathlib import Path


#############################################################
#
# functions for preparing the preference profile

# Print pref orders
# m n (number of candidates and voters)
# m lines with candidate names (number position)
# n lines with preference orders (followed by positions)
from aaa_pb.model.ballot_calc import BallotCalc


def printPrefOrders(C, V, P, output_file):
    m = len(C)
    n = len(V)

    output_file.write("{0} {1}\n".format(m, n))

    for i in range(len(C)):
        line = "{0}  {1} {2} {3}\n".format(i, C[i][0], C[i][1], C[i][2])
        output_file.write(line)

    for i in range(len(P)):
        joined = " ".join([str(p) for p in P[i]])
        line = "{0} {1} {2}\n".format(V[i][0], V[i][1], joined)
        output_file.write(line)


# read in the data in our format
# m n  (number of candidates and voters)
# x  y (m candidates in m lines)
# ...
# x  y (n voters in n lines)
# ...

# return (m, n, C, P)

def parse2dPointsData(lines):
    # type: (list[str]) -> (int, int, list[(float, float, str)], list[(float, float)])
    P = []
    C = []
    (m, n) = lines[0].split()
    m = int(m)
    n = int(n)

    for l in lines[1:m + 1]:
        (x, y, p) = l.split()
        C += [(float(x), float(y), p)]

    for l in lines[m + 1:m + n + 1]:
        (x, y, ignored) = l.split()
        P += [(float(x), float(y))]

    return m, n, C, P


def dist(x, y):
    return (sum([(x[i] - y[i]) ** 2 for i in range(len(x))])) ** (0.5)


# Compute the distances of voter v from the candidates in set C
# outputs a list of the format (i,d) where i is the candidate
# name and d is the distance
#
def computeDistances(v, C):
    m = len(C)
    d = [(j, dist(v, C[j])) for j in range(m)]
    return d


def second(x):
    return x[1]


# TODO PBATKO test it!
def takeNClosestCandidates(v, C, n, at_least_one=True):
    v_dist = computeDistances(v, C)
    v_dist_sorted = sorted(v_dist, key=second)
    v_selected = [cand for (cand, dis) in v_dist_sorted][:n]

    if at_least_one and len(v_selected) == 0:
        return [v_dist_sorted[0][0]]

    return v_selected


# TODO PBATKO test it!
def takeAllInRadius(v, C, radius, at_least_one=True):
    v_dist = computeDistances(v, C)
    v_dist_sorted = sorted(v_dist, key=second)
    v_selected = [cand for (cand, dis) in v_dist_sorted if dis <= radius]

    if at_least_one and len(v_selected) == 0:
        return [v_dist_sorted[0][0]]

    return v_selected


class OrdinalBallotCalc(BallotCalc):

    def getShortName(self):
        return "ord"

    def serializeToString(self):
        return "ord"

    # MAIN

    def calculateFrom2dPoints(self, C, V):
        # type: (list[(float, float)], list[(float, float)]) -> list[list[int]]
        P = self.__calculatePreferenceOrders(C, V)
        return P

    def calculateFrom2PointsFile(self, input_file_path, output_file_path):
        # type: (Path, Path) -> None
        with open(str(input_file_path), 'r') as input_file, \
                open(str(output_file_path), 'w') as output_file:
            lines = input_file.readlines()
            (m, n, C, V) = parse2dPointsData(lines)
            P = self.__calculatePreferenceOrders(C, V)
            printPrefOrders(C, V, P, output_file)
            output_file.close()

    @staticmethod
    def __calculatePreferenceOrders(C, V):
        # type: (list[(float, float, str)], list[(float, float)]) -> list[list[int]]
        P = []
        #  print C
        for v in V:
            v_dist = computeDistances(v, C)
            v_sorted = sorted(v_dist, key=second)
            v_order = [cand for (cand, dis) in v_sorted]
            P += [v_order]
        return P

    pass


def drawRandomPositiveGauss(mean, sigma, max_loops=10):
    l = 0
    while l < max_loops:
        l += 1
        radius = random.gauss(mean, sigma)
        if radius > 0:
            return radius
    else:
        raise Exception(
            "Exceeded loop limit when trying to draw positive number from gaussion(m={0},s={1}".format(mean, sigma))


class ApprovalBallotCalc(BallotCalc):

    __ballotCalcs = {}

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self._get_params() == other._get_params()
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def register(cls):
        # type: () -> None
        cls.__ballotCalcs[cls.__name__] = cls


    @classmethod
    def fromString(cls, name: str, params: List[str]) -> 'ApprovalBallotCalc':
        float_params = [float(x) for x in params]
        return cls.__ballotCalcs[name](*float_params)

    @classmethod
    def to_json_repr(cls, approval_ballot: 'ApprovalBallotCalc') -> Dict[str, str]:
        pass

    def __init__(self, calculate_approved_set_fun, short_name):
        self.calculate_approved_set_fun = calculate_approved_set_fun
        self.short_name = short_name

    def getShortName(self):
        return self.short_name

    def calculateFrom2dPoints(self, C, V):
        # type: (list[(float, float)], list[(float, float)]) -> list[list[int]]
        P = self.calculate_approved_set_fun(C, V)
        return P

    def calculateFrom2PointsFile(self, input_file_path, output_file_path):
        # type: (Path, Path) -> None

        with open(str(input_file_path), 'r') as input_file, \
                open(str(output_file_path), 'w') as output_file:
            lines = input_file.readlines()
            (m, n, C, V) = parse2dPointsData(lines)
            P = self.calculate_approved_set_fun(C, V)
            printPrefOrders(C, V, P, output_file)
            output_file.close()

    pass


class ApprovalBallotCalc_NearestGauss(ApprovalBallotCalc):

    def serializeToString(self):
        return "\n".join(["app_nearest_guass", str(2), self.mean, self.sigma])

    def __init__(self, mean, sigma):
        self.mean = mean
        self.sigma = sigma
        super(ApprovalBallotCalc_NearestGauss, self).__init__(
            calculate_approved_set_fun=(self.__get_fun(mean, sigma)),
            short_name="nearest-gauss{0}-{1}".format(mean, sigma)
        )

    def _get_params(self):
        return [self.mean, self.sigma]

    @classmethod
    def __get_fun(clazz, mean, sigma):
        def fun(C, V):
            # type: (list[(float, float, str)], list[(float, float)]) -> list[list]
            P = []
            for v in V:
                take_n = int(drawRandomPositiveGauss(mean, sigma))
                approved_candidates = takeNClosestCandidates(v, C, take_n)

                P += [approved_candidates]
            return P

        return fun

    pass

ApprovalBallotCalc_NearestGauss.register()

class ApprovalBallotCalc_NearestUniform(ApprovalBallotCalc):

    def to_dict(self):
        # type: () -> dict
        return {'min': self.min,
                'max': self.max
                }

    @classmethod
    def from_dict(self, d):
        # type: (dict) -> ApprovalBallotCalc_NearestUniform
        return ApprovalBallotCalc_NearestUniform(**d)


    def __init__(self, min, max):
        self.min = min
        self.max = max
        super(ApprovalBallotCalc_NearestUniform, self).__init__(
            calculate_approved_set_fun=(self.__get_fun(min, max)),
            short_name="nearest-uniform{0}-{1}".format(min, max)
        )


    def _get_params(self):
        return [self.min, self.max]

    @classmethod
    def __get_fun(clazz, min, max):
        def fun(C, V):
            # type: (list[(float, float, str)], list[(float, float)]) -> list[list]
            P = []
            for v in V:
                take_n = random.randint(min, max)
                approved_candidates = takeNClosestCandidates(v, C, take_n)

                P += [approved_candidates]
            return P

        return fun

    pass

ApprovalBallotCalc_NearestUniform.register()

class ApprovalBallotCalc_RadiusUniform(ApprovalBallotCalc):

    def serializeToString(self):
        return "ord_radius_uniform"

    def __init__(self, min, max):
        self.min = min
        self.max = max
        super(ApprovalBallotCalc_RadiusUniform, self).__init__(
            calculate_approved_set_fun=(self.__get_fun(min, max)),
            short_name="radius-uniform{0}-{1}".format(min, max)
        )

    def _get_params(self):
        return [self.min, self.max]

    @classmethod
    def __get_fun(clazz, min, max):
        def fun(C, V):
            # type: (list[(float, float, str)], list[(float, float)]) -> list[list]
            P = []
            for v in V:
                radius = random.uniform(min, max)
                approved_candidates = takeAllInRadius(v, C, radius)

                P += [approved_candidates]
            return P

        return fun

    pass

ApprovalBallotCalc_RadiusUniform.register()

class ApprovalBallotCalc_RadiusGauss(ApprovalBallotCalc):

    def serializeToString(self):
        return "ord_radius_gauss"

    def __init__(self, mean, sigma):
        self.mean = mean
        self.sigma = sigma
        super(ApprovalBallotCalc_RadiusGauss, self).__init__(
            calculate_approved_set_fun=(self.__get_fun(mean, sigma)),
            short_name="radius-gauss{0}-{1}".format(mean, sigma)
        )

    def _get_params(self):
        return [self.mean, self.sigma]

    @classmethod
    def __get_fun(clazz, mean, sigma):
        def fun(C, V):
            # type: (list[(float, float, str)], list[(float, float)]) -> list[list]
            P = []
            for v in V:
                radius = drawRandomPositiveGauss(mean, sigma)
                approved_candidates = takeAllInRadius(v, C, radius)

                P += [approved_candidates]
            return P

        return fun

ApprovalBallotCalc_RadiusGauss.register()

# if __name__ == "__main__":
#
#     if (len(argv) != 3):
#         print "This script converts an election in the 2D Euclidean format to a preference-order based one"
#         print
#         print "Invocation:"
#         print "  python 2d2pref.py  2d_point.in election.out"
#         exit(1)
#
#     input_file_path = Path(argv[1])
#     output_file_path = Path(argv[2])
#
#     OrdinalBallotCalc.calculateFrom2PointsFile(input_file_path, output_file_path)
