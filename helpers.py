from random import *
from enum import Enum
import os


image_import_fail = False
try:
    from PIL import Image
except ImportError:
    print("PIL module is not available. Pictures will not be generated.")
    image_import_fail = True


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
            raise OSError("Directory already exists.")


def print_or_save(id, value, data_out=None):
    result = "{} {}".format(str(id), ' '.join(map(str, value)))
    if data_out is None:
        print(result)
    else:
        data_out.write(result + '\n')

# GENERATE POINTS


def generate_from_image(filename, x1, y1, x2, y2, N, party):

    img = Image.open(os.path.join(filename))
    rgb_im = img.convert('RGB')

    x, y = rgb_im.size
    density_map = []
    total_color_intensity = 0
    for i in range(x):
        for j in range(y):
            pixel = rgb_im.getpixel((i, j))
            color_intensity = (255 - pixel[0]) + (255 - pixel[1]) + (255 - pixel[2])
            coor1 = x1 + (float(i * (x2 - x1)) / x)
            coor2 = y2 - (float(j * (y2 - y1)) / y)
            density_map.append((coor1, coor2, color_intensity))
            total_color_intensity += color_intensity
    random_list = [random() * total_color_intensity for _ in range(N)]
    result = []
    i = 0
    passed_intensity = 0
    for v in sorted(random_list):
        while passed_intensity < v:
            passed_intensity += density_map[i][2]
            i += 1
        result.append((density_map[i][0], density_map[i][1], party))
    return result


def generate_uniform(x1, y1, x2, y2, N, party):
    (x1, x2) = (min(x1, x2), max(x1, x2))
    (y1, y2) = (min(y1, y2), max(y1, y2))
    return [(random() * (x2 - x1) + x1, random() * (y2 - y1) + y1, party) for _ in range(N)]


def generate_gauss(x, y, sigma, N, party):
    return [(gauss(x, sigma), gauss(y, sigma), party) for _ in range(N)]


def generate_circle(x, y, r, N, party):
    count = 0
    L = []
    while count < N:
        (px, py) = (random() * (2 * r) - r, random() * (2 * r) - r)
        if px ** 2 + py ** 2 <= r ** 2:
            L += [(px + x, py + y, party)]
            count += 1
    return L


def impartial(m, n):
    # preferences
    candidates = list(range(m))
    voters = []

    for p in range(n):
        x = list(range(m))
        shuffle(x)
        voters += [x]

    return candidates, voters


# read in the data in our format
# m n  (number of candidates and voters)
# x  y (m candidates in m lines)
# ...
# x  y (n voters in n lines)
# ...
# assume that dim(Ci) = dim(Vj) for i in C, j in V

# return (candidates, preferences)
def read_data(f):
    P = []
    C = []
    V = []
    lines = f.readlines()
    (m, n) = lines[0].split()
    m = int(m)
    n = int(n)

    for l in lines[1:m + 1]:
        row = l.split()
        C.append(tuple(map(float, row[:-1])) + (row[-1], ))

    dim = len(C[0])
    if isinstance(C[0], str):
        dim -= 1
    for l in lines[m + 1:m + n + 1]:
        # print("Line", l.split())
        row = l.split()
        preferences = row[:-dim]
        voter = row[1 - dim:]
        P.append(list(map(float, preferences)))
        V.append(voter)

    return C, V, P


