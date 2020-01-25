from enum import Enum
import os


class Command(Enum):
    GEN_CANDIDATES = 1
    GEN_VOTERS = 2
    GEN_FROM_CANDIDATES = 3
    IMPARTIAL = 4


def make_dirs(dir_path, exist_ok=False):
    path_exists = os.path.exists(dir_path)
    if exist_ok:
        if not path_exists:
            os.makedirs(dir_path)
    else:
        if path_exists:
            raise OSError('Directory already exists.')


def print_or_save(object_id, value, data_out=None):
    result = "{} {}".format(str(object_id), ' '.join(map(str, value)))
    if data_out is None:
        print(result)
    else:
        data_out.write(result + '\n')


# read in the data in our format
# m n k  (number of candidates and voters, committee size)
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
    parameters = lines[0].split()
    k = 0
    if len(parameters) == 2:
        with_winners = False
        m, n = parameters
    elif len(parameters) == 3:
        with_winners = True
        m, n, k = parameters
    else:
        raise Exception('Invalid .win file format!')

    m = int(m)
    n = int(n)
    k = int(k)

    for l in lines[1:m + 1]:
        row = l.split()
        candidates.append(tuple(map(float, row[:-1])) + (row[-1],))

    dim = len(candidates[0])
    if isinstance(candidates[0], str):
        dim -= 1
    for l in lines[m + 1:m + n + 1]:
        row = l.split()
        preference = row[:-dim]
        voter = row[1 - dim:]
        preferences.append(list(map(float, preference)))
        voters.append(voter)

    if with_winners:
        winners = []
        for l in lines[1 + n + m: 1 + n + m + k]:
            row = l.split()
            winners.append(int(row[0]))

        return candidates, voters, preferences, winners
    else:
        return candidates, voters, preferences


def process_win_dir(path, strategy):
    """
    :param path: path of processed directory
    :type path: str
    :param strategy: Run with (candidates, voters, winners, election)
    :type strategy: Callable
    """
    for root, dirs, file_names in os.walk(path):
        depth = len(root.split('/'))

        if depth == 2:
            win_files = [fname for fname in file_names if fname.split('.')[-1] == 'win']
            election = root.split('/')[-1]

            for fname in win_files:
                f = open(os.path.join(root, fname), 'r')
                candidates_list, voters_list, _, winners_list = read_data(f)

                strategy(candidates=candidates_list, voters=voters_list, winners=winners_list, election=election)
