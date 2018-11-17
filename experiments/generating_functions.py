import os
from random import random, gauss, shuffle

from preferences.ordinal import Ordinal

image_import_fail = False
try:
    from PIL import Image
except (ImportError, NameError):
    print("PIL module is not available. Pictures will not be generated.")
    image_import_fail = True

# GENERATE POINTS


def generate_from_image(filename, x1, y1, x2, y2, n, party):

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
    random_list = [random() * total_color_intensity for _ in range(n)]
    result = []
    i = 0
    passed_intensity = 0
    for v in sorted(random_list):
        while passed_intensity < v:
            passed_intensity += density_map[i][2]
            i += 1
        result.append((density_map[i][0], density_map[i][1], party))
    return result


def generate_uniform(x1, y1, x2, y2, n, party):
    (x1, x2) = (min(x1, x2), max(x1, x2))
    (y1, y2) = (min(y1, y2), max(y1, y2))
    return [(random() * (x2 - x1) + x1, random() * (y2 - y1) + y1, party) for _ in range(n)]


def generate_gauss(x, y, sigma, n, party):
    return [(gauss(x, sigma), gauss(y, sigma), party) for _ in range(n)]


def generate_circle(x, y, r, n, party):
    count = 0
    l = []
    while count < n:
        (px, py) = (random() * (2 * r) - r, random() * (2 * r) - r)
        if px ** 2 + py ** 2 <= r ** 2:
            l += [(px + x, py + y, party)]
            count += 1
    return l


def impartial(m, n):
    # preferences
    candidates = list(range(m))
    voters = []

    for p in range(n):
        x = list(range(m))
        shuffle(x)
        voters += [x]
    preferences = [Ordinal(voter) for voter in voters]
    return candidates, voters, preferences
