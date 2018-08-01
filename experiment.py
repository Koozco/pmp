import os
from os import system
from random import *
from sys import *
from visualize import *
from winner import winner

image_import_fail = False
try:
    from PIL import Image
except ImportError:
    print("PIL module is not available. Pictures will not be generated.")
    image_import_fail = True


import pref2d2

# used for 2D
C = []
V = []

# used for non-2D
REAL_C = []
REAL_V = []

DATA = "C"
NAME = "data"
TWO_DIMENSIONAL = True


# TODO: change files structure
# TODO: refactor
# TODO: think about where to put the files

# GENERATE POINTS

def generateFromImage(filename, x1, y1, x2, y2, N, Party):
    # dir_path = os.path.join("..", "in")
    dir_path = os.path.join("..")
    try:
        os.makedirs(dir_path)
    except OSError:
        if not os.path.isdir(dir_path):
            raise

    img = Image.open(os.path.join(dir_path, filename))
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
        result.append((density_map[i][0], density_map[i][1], Party))
    return result


def generateUniform(x1, y1, x2, y2, N, Party):
    (x1, x2) = (min(x1, x2), max(x1, x2))
    (y1, y2) = (min(y1, y2), max(y1, y2))
    return [(random() * (x2 - x1) + x1, random() * (y2 - y1) + y1, Party) for _ in range(N)]


def generateGauss(x, y, sigma, N, Party):
    return [(gauss(x, sigma), gauss(y, sigma), Party) for _ in range(N)]


def generateCircle(x, y, r, N, Party):
    count = 0
    L = []
    while count < N:
        (px, py) = (random() * (2 * r) - r, random() * (2 * r) - r)
        if px ** 2 + py ** 2 <= r ** 2:
            L += [(px + x, py + y, Party)]
            count += 1
    return L


# save data

def saveData(name):
    global TWO_DIMENSIONAL
    global REAL_C
    global REAL_V

    if TWO_DIMENSIONAL:
        # dir_path = os.path.join("..", "in") # TODO: make this path an argument or save to default location
        dir_path = os.path.join("..")
        try:
            os.makedirs(dir_path)
        except OSError:
            if not os.path.isdir(dir_path):
                raise

        # f = open(os.path.join(dir_path, name + ".in"), "w")
        f = open(name + ".in", "w")
        m = len(C)
        n = len(V)
        f.write("{} {}\n".format(m, n))
        for p in C:
            f.write("{} {} {}\n".format(p[0], p[1], p[2]))
        for p in V:
            f.write("{} {} {}\n".format(p[0], p[1], p[2]))
        f.close()

        pref2d2.pref(str(name + ".in"), str(name + ".out"))
        # system("python pref2d2.py <%s.in >%s.out" % (name, name))

    else:
        dir_path = os.path.join("..", "out")
        try:
            os.makedirs(dir_path)
        except OSError:
            if not os.path.isdir(dir_path):
                raise

        f = open(os.path.join(dir_path, name + ".out"), "w")
        f.write("{} {}".format(len(REAL_C), len(REAL_V)))
        for c in REAL_C:
            f.write(c)
        for v in REAL_V:
            s = ""
            for z in v:
                s += str(z) + " "
            f.write(s)
        f.close()


def impartial(M, N):
    global REAL_C
    global REAL_V

    REAL_C = range(M)

    for p in range(N):
        x = range(M)
        shuffle(x)
        REAL_V += [x]


# compute winners

def computeWinners(rule, k, output):
    global NAME
    # system("python winner.py <%s.out >%s.win %s %d" % (NAME, output, rule, k))
    winner(NAME + ".out", output + ".win", rule, k)
    if TWO_DIMENSIONAL:
        print("2D = " + str(TWO_DIMENSIONAL))
        if image_import_fail:
            print("Cannot visualize results because of PIL import fail.")
            return
        visualize(output)  # TODO: make it work from console as well
        # system("python visualize.py {}".format(output))  # to delete


def getOrNone(l, n):
    try:
        return l[n]
    except:
        return "NONE"


# COMMAND EXECUTION

def execute(command):
    global DATA
    global NAME
    global TWO_DIMENSIONAL
    print(command)
    if command[0] == "candidates":
        DATA = "C"
    elif command[0] == "voters":
        DATA = "V"
    elif command[0] == "circle":
        P = generateCircle(float(command[1]), float(command[2]), float(command[3]), int(command[4]),
                           getOrNone(command, 5))
        X = eval(DATA)
        X += P
    elif command[0] == "gauss":
        P = generateGauss(float(command[1]), float(command[2]), float(command[3]), int(command[4]),
                          getOrNone(command, 5))
        X = eval(DATA)
        X += P
    elif command[0] == "uniform":
        P = generateUniform(float(command[1]), float(command[2]), float(command[3]), float(command[4]), int(command[5]),
                            getOrNone(command, 6))
        X = eval(DATA)
        X += P
    elif command[0] == "image":
        if image_import_fail:
            return
        P = generateFromImage(command[1], float(command[2]), float(command[3]), float(command[4]), float(command[5]),
                              int(command[6]), getOrNone(command, 7))
        X = eval(DATA)
        X += P
    elif command[0] == "generate":
        NAME = command[1]
        saveData(NAME)

    elif command[0] == "impartial":
        TWO_DIMENSIONAL = False
        impartial(int(command[1]), int(command[2]))

    elif command[0] == "#":
        None
    else:
        computeWinners(command[0], int(command[1]), command[2])


# READ DATA IN
def readData(f):
    cmd = []
    lines = f.readlines()

    for l in lines:
        s = l.split()
        if len(s) > 0:
            cmd += [s]

    return cmd


# MAIN

if __name__ == "__main__":

    if len(argv) > 1:
        print("This scripts runs a single experiment (generates an elections, "
              "\ncomputes the results accoring to specified rules, and prepares visualizations)")
        print("\nInvocation:")
        print("  python experiment.py  <description.input")
        exit()

    seed()

    data_in = stdin
    data_out = stdout

    cmd = readData(data_in)

    for command in cmd:
        if not command[0].lstrip()[0] == '#':
            execute(command)
