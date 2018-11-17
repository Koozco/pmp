import os

pil_import_fail = False
try:
    from PIL import Image, ImageDraw
    from PIL import ImageColor
except (ImportError, NameError):
    print("Cannot import PIL.")
    pil_import_fail = True

DIMENSION = 2
WIDTH = 600
HEIGHT = 600


def dist(x, y):
    return (sum([(x[i] - y[i]) ** 2 for i in range(DIMENSION)])) ** 0.5


# Computes distances of the voters to the closest members of the committee
def compute_dist(voters, winners, candidates):
    d = 0.0
    max_dist = 0.0
    n = 0
    for v in voters:
        dmin = float("inf")
        for w in winners:
            dmin = min(dmin, dist(v, candidates[w]))
        d += dmin
        max_dist = max(max_dist, dmin)
        n += 1
    return d / n, max_dist


# Computes distance of each committee member to the closest n/k voters
def compute_dist_of_representatives_to_virt_districts(voters, winners, candidates):
    n = len(voters)
    k = len(winners)
    d = 0.0
    max_dist = 0.0
    for w in winners:
        distances = []
        dmin = 0.0
        for v in voters:
            distances.append(dist(v, candidates[w]))
        for val in sorted(distances)[: int(n / k)]:
            dmin += val
        d += dmin
        max_dist = max(max_dist, dmin)
    return d / k, max_dist


def compute_winners_per_party(candidates, winners):
    result = {}
    for c in candidates:
        party = c[-1]
        if party not in result.keys():
            result[party] = 0
    for w in winners:
        party = candidates[w][-1]
        result[party] += 1
    return result


def visualize(candidates, voters, winners, name, path):

    avg_d, max_d = compute_dist(voters, winners, candidates)
    rep_avg_d, rep_max_d = compute_dist_of_representatives_to_virt_districts(voters, winners, candidates)
    per_party = compute_winners_per_party(candidates, winners)

    with open(os.path.join(path, "stats.out"), "a") as stats_out:
        stats_out.write(name + ": \n")
        stats_out.write("  avg_d = " + str(avg_d) + "\n")
        stats_out.write("  max_d = " + str(max_d) + "\n")
        stats_out.write("  rep_avg_d = " + str(rep_avg_d) + "\n")
        stats_out.write("  rep_max_d = " + str(rep_max_d) + "\n")
        for (p, v) in per_party.items():
            stats_out.write("  party-" + str(p) + " = " + str(v) + "\n")

    if pil_import_fail:
        print("Cannot use functions from PIL")
        return
    im = Image.new("RGB", (WIDTH, HEIGHT), "white")
    dr = ImageDraw.Draw(im)

    hx = 2
    hy = 2

    dr.line((0, HEIGHT / 2, WIDTH, HEIGHT / 2), fill=128)
    dr.line((WIDTH / 2, 0, WIDTH / 2, HEIGHT), fill=128)
    for z in candidates:
        dr.ellipse((WIDTH / 2 + z[0] * 100 - hx, HEIGHT / 2 - z[1] * 100 - hy, WIDTH / 2 + z[0] * 100 + hx,
                    HEIGHT / 2 - z[1] * 100 + hy),
                   fill="rgb(220,220,220)")

    hx = 2
    hy = 2

    dr.line((0, HEIGHT / 2, WIDTH, HEIGHT / 2), fill=128)
    dr.line((WIDTH / 2, 0, WIDTH / 2, HEIGHT), fill=128)
    for z in voters:
        dr.ellipse((WIDTH / 2 + z[0] * 100 - hx, HEIGHT / 2 - z[1] * 100 - hy, WIDTH / 2 + z[0] * 100 + hx,
                    HEIGHT / 2 - z[1] * 100 + hy), fill="rgb(150,150,150)")

    wx = 5
    wy = 5
    for z in winners:
        c = candidates[z]
        dr.ellipse((WIDTH / 2 + c[0] * 100 - wx, HEIGHT / 2 - c[1] * 100 - wy, WIDTH / 2 + c[0] * 100 + wx,
                    HEIGHT / 2 - c[1] * 100 + wy), fill="red")

    dr.text((0, 0), name + " (%d out of %d)" % (len(winners), len(candidates)), fill="blue")

    im.save(os.path.join(path, name + ".png"))
