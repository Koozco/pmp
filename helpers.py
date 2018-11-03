from random import *
import os

image_import_fail = False
try:
    from PIL import Image
except ImportError:
    print("PIL module is not available. Pictures will not be generated.")
    image_import_fail = True


def make_dirs(dir_path, exist_ok=False):
    path_exists = os.path.exists(dir_path)
    if exist_ok:
        if not path_exists:
            os.makedirs(dir_path)
    else:
        if path_exists:
            raise OSError("Directory already exists.")


def print_or_save(id, value, data_out=None):
    if data_out is None:
        print(id, value)
    else:
        data_out.write("{} {}\n".format(str(id), ' '.join(map(str, value))))

# GENERATE POINTS


def generateFromImage(filename, x1, y1, x2, y2, N, party):

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
