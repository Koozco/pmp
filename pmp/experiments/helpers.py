from enum import Enum
import os


class Command(Enum):
    GEN_CANDIDATES = 1
    GEN_VOTERS = 2
    GEN_FROM_CANDIDATES = 3
    IMPARTIAL = 4


class ExperimentElectionConfig:
    def __init__(self, rule, k, filename):
        self.rule = rule
        self.k = k
        self.filename = filename


def make_dirs(dir_path, exist_ok=False):
    path_exists = os.path.exists(dir_path)
    if exist_ok:
        if not path_exists:
            os.makedirs(dir_path)
    else:
        if path_exists:
            raise OSError("Directory already exists.")


def print_or_save(object_id, value, data_out=None):
    result = "{} {}".format(str(object_id), ' '.join(map(str, value)))
    if data_out is None:
        print(result)
    else:
        data_out.write(result + '\n')


# read in the data in our format
# m n  (number of candidates and voters)
# x  y (m candidates in m lines)
# ...
# x  y (n voters in n lines)
# ...
# assume that dim(Ci) = dim(Vj) for i in C, j in V

# return (candidates, preferences)
def read_data(f):
    preferences = []
    candidates = []
    voters = []
    lines = f.readlines()
    (m, n) = lines[0].split()
    m = int(m)
    n = int(n)

    for l in lines[1:m + 1]:
        row = l.split()
        candidates.append(tuple(map(float, row[:-1])) + (row[-1], ))

    dim = len(candidates[0])
    if isinstance(candidates[0], str):
        dim -= 1
    for l in lines[m + 1:m + n + 1]:
        row = l.split()
        preference = row[:-dim]
        voter = row[1 - dim:]
        preferences.append(list(map(float, preference)))
        voters.append(voter)

    return candidates, voters, preferences
