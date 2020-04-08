from sys import *

from PIL import Image, ImageDraw
from pathlib import Path

DIMENSION = 2


def perhapsFloat(v):
    try:
        return float(v)
    except:
        return v


def readData(f):
    lines = f.readlines()

    (m, n, k) = lines[0].split()
    m = int(m)
    n = int(n)
    k = int(k)

    C = []
    V = []
    W = []

    for l in lines[1:m + 1]:
        s = l.split()[1:] # omit first item - it's just candidate name
        s = [perhapsFloat(x) for x in s]
        C += [s]

    for l in lines[m + 1:m + n + 1]:
        s = l.split()[:2] # first two items are voter coordinates
        s = [float(x) for x in s]
        V += [s]

    for l in lines[n + m + 1:n + m + k + 1]:
        s = l.split()[1:]
        s = [perhapsFloat(x) for x in s]
        W += [s]

    #  print len(C)
    #  print C
    #  print "---"
    #  print V
    #  print "---"
    #  print W

    return (m, n, k, C, V, W)


def dist(x, y):
    return (sum([(x[i] - y[i]) ** 2 for i in range(DIMENSION)])) ** (0.5)


# Computes distances of the voters to the closest members of the committee
def compute_dist(V, Winners):
    d = 0.0
    max_dist = 0.0
    n = 0
    for v in V:
        dmin = float("inf")
        for w in Winners:
            dmin = min(dmin, dist(v, w))
        d += dmin
        max_dist = max(max_dist, dmin)
        n += 1
    return d / n, max_dist


# Computes distance of each committee member to the closest n/k voters
def compute_dist_of_representatives_to_virt_districts(V, Winners):
    n = len(V)
    k = len(Winners)
    d = 0.0
    max_dist = 0.0
    for w in Winners:
        distances = []
        dmin = 0.0
        for v in V:
            distances.append(dist(v, w))
        for val in sorted(distances)[: int(n / k)]:
            dmin += val
        d += dmin
        max_dist = max(max_dist, dmin)
    return d / k, max_dist


def compute_winners_per_party(C, W):
    result = {}
    for c in C:
        party = c[-1]
        if party not in result.keys():
            result[party] = 0
    for w in W:
        party = w[-1]
        result[party] += 1
    return result


def append_to_stats_file(stats_out_file, input_file_arg, avg_d, max_d, rep_avg_d, rep_max_d, perParty):
    stats_out_file.write(input_file_arg + ": \n")
    stats_out_file.write("  avg_d = " + str(avg_d) + "\n")
    stats_out_file.write("  max_d = " + str(max_d) + "\n")
    stats_out_file.write("  rep_avg_d = " + str(rep_avg_d) + "\n")
    stats_out_file.write("  rep_max_d = " + str(rep_max_d) + "\n")
    for (p, v) in perParty.iteritems():
        stats_out_file.write("  party-" + str(p) + " = " + str(v) + "\n")
    stats_out_file.close()


def drawImage(V, C, Winner, rule_name):
    W = 600
    H = 600
    im = Image.new("RGB", (W, H), "white")
    dr = ImageDraw.Draw(im)
    hx = 2
    hy = 2
    dr.line((0, H / 2, W, H / 2), fill=128)
    dr.line((W / 2, 0, W / 2, H), fill=128)
    for z in C:
        dr.ellipse((W / 2 + z[0] * 100 - hx, H / 2 - z[1] * 100 - hy, W / 2 + z[0] * 100 + hx, H / 2 - z[1] * 100 + hy),
                   fill="rgb(220,220,220)")
    #  print z
    hx = 2
    hy = 2
    dr.line((0, H / 2, W, H / 2), fill=128)
    dr.line((W / 2, 0, W / 2, H), fill=128)

    for z in V:
        z_hx = W / 2 + z[0] * 100 - hx
        z_hy = H / 2 - z[1] * 100 - hy
        w_z_hx = W / 2 + z[0] * 100 + hx
        h_z_hy = H / 2 - z[1] * 100 + hy
        dr.ellipse((z_hx, z_hy, w_z_hx, h_z_hy), fill="rgb(150,150,150)")
    #  print z
    wx = 5
    wy = 5
    for z in Winner:
        dr.ellipse((W / 2 + z[0] * 100 - wx, H / 2 - z[1] * 100 - wy, W / 2 + z[0] * 100 + wx, H / 2 - z[1] * 100 + wy),
                   fill="red")
    #  print z
    dr.text((0, 0), rule_name + " (%d out of %d)" % (len(Winner), len(C)), fill="blue")

    return im


def drawVisualization(img_file_output_path, input_file_path, rule_name):
    with open(str(input_file_path), "r") as data_in:
        (m, n, k, C, V, Winner) = readData(data_in)

    drawVisualizationSane(C, V, Winner, img_file_output_path, rule_name)


def drawVisualizationSane(C, V, Winner, img_file_output_path: Path, rule_name):
    image = drawImage(V, C, Winner, rule_name)
    image.save(str(img_file_output_path))


if __name__ == "__main__":
    # data_in = open(argv[1] + ".win", "r")
    input_file_arg = argv[1]  # .win file
    output_dir_arg = argv[2]

    rule_name = None # TODO PBATKO
    # TODO PBATKO stats doesn't work with approval ballots, fix it
    # calc
    # avg_d, max_d = compute_dist(V, Winner)
    # rep_avg_d, rep_max_d = compute_dist_of_representatives_to_virt_districts(V, Winner)
    # perParty = compute_winners_per_party(C, Winner)
    # stats
    # stats_out_file_path = Path(output_dir_arg) / "stats.out"
    # stats_out_file = open(str(stats_out_file_path), "a")
    # append_to_stats_file(stats_out_file, input_file_arg, avg_d, max_d, rep_avg_d, rep_max_d, perParty)

    # image
    img_file_output_path = Path(output_dir_arg) / (input_file_arg + ".png")
    input_file_path = Path(input_file_arg)

    drawVisualization(img_file_output_path, input_file_path, rule_name)
