from sys import *
from math import *
from PIL import Image, ImageDraw
from PIL import ImageColor

from aaa_pb.utils.path_validator import PathValidator


def readData(lines):
    # type: (list[str]) -> object

    (W, H) = lines[0].split()
    W = int(W)
    H = int(W)
    # hx = 1
    # hy = 1

    HISTOGRAM = []

    for l in lines[1:H + 1]:
        s = l.split()
        s = [int(v) / 10.0 for v in s]
        HISTOGRAM += [s]

    return (W, H, HISTOGRAM)


def drawWithLocalNormalization(H, W, HISTOGRAM, MAX, dr):
    print("LOCAL NORMALIZATION")
    for y in range(H):
        for x in range(W):
            if (HISTOGRAM[y][x] > 0):
                inte = 255 - int(255 * (float(HISTOGRAM[y][x]) / MAX))
                #      dr.ellipse( (x-hx, y-hy, x+hx, y+hy), fill= "rgb(255,%d,%d)" % (inte,inte)  )
                dr.point((x, (H - 1) - y), fill="rgb(255,%d,%d)" % (inte, inte))


def drawWithGlobalNormalization(H, W, HISTOGRAM, TOTAL, threshold, col_r, col_g, col_b, dr):
    MAX_VAL = 0.0
    # hx = 1
    # hy = 1
    #  threshold = 0.0005
    print("GLOBAL NORMALIZATION")
    # test = 0
    for y in range(H):
        for x in range(W):
            if (HISTOGRAM[y][x] > 0):
                inte = float(HISTOGRAM[y][x]) / TOTAL
                #        if( inte > threshold ):
                #          dr.point( (x,(H-1)-y), fill= "rgb(128,255,128)"  )
                #          test += 1
                #        else:
                val = float(inte) / threshold
                MAX_VAL = max(val, MAX_VAL)
                val = (atan(val)) / (pi / 2)
                #        val = log(1+val)
                #        val = min(1.0, val)

                ####        val = 255-int(val*255)
                #        dr.point( (x,(H-1)-y), fill= "rgb(%d,%d,255)" % (val,val)  )
                dr.point((x, (H - 1) - y), fill="rgb(%d,%d,%d)" % (
                255 - 255 * (col_r * val), 255 - 255 * (col_g * val), 255 - 255 * (col_b * val)))
    #        inte = 255-int(255*(    float(HISTOGRAM[y][x]) / MAX) )
    #        dr.ellipse( (x-hx, y-hy, x+hx, y+hy), fill= "rgb(255,%d,%d)" % (inte,inte)  )
    print("MAX_VAL = ", MAX_VAL)


def drawHistogram(output_dir_path, input_file_path, output_file_name, TRADITIONAL, threshold, col_r, col_g, col_b):
    output_path = output_dir_path / output_file_name
    drawHistogramSaner1(output_path, input_file_path,  TRADITIONAL, threshold, col_r, col_g, col_b)
    pass


def drawHistogramSaner1(output_file_path, input_file_path, TRADITIONAL, threshold, col_r, col_g, col_b):

    with open(str(input_file_path), "r") as input_file:
        lines = input_file.readlines()
    (W, H, HISTOGRAM) = readData(lines)

    drawHistogramSaner2(output_file_path, W, H, HISTOGRAM, TRADITIONAL, threshold, col_r, col_g, col_b)

    pass


def drawHistogramSaner2(output_file_path, W, H, HISTOGRAM, TRADITIONAL, threshold, col_r, col_g, col_b):

    TOTAL = 0
    MAX = 0
    for y in range(H):
        for x in range(W):
            TOTAL += HISTOGRAM[y][x]
            if HISTOGRAM[y][x] > MAX:
                MAX = HISTOGRAM[y][x]
    print("DRAWING, TOTAL = %d" % TOTAL)

    im = Image.new("RGB", (W, H), "white")
    dr = ImageDraw.Draw(im)
    dr.line((0, H / 2, W, H / 2), fill=128)
    dr.line((W / 2, 0, W / 2, H), fill=128)

    if (TRADITIONAL):
        drawWithLocalNormalization(H, W, HISTOGRAM, MAX, dr)
    else:
        drawWithGlobalNormalization(H, W, HISTOGRAM, TOTAL, threshold, col_r, col_g, col_b, dr)

    im.save(str(output_file_path))


if __name__ ==  '__main__':

    print("LOADING...", argv[1])

    if len(argv) != 4:
        print("Expected 3 arguments, actual: {0}!".format(len(argv)-1))
        exit(1)

    output_dir_path = PathValidator(argv[1], "Output dir") \
        .exists() \
        .is_dir() \
        .get_path()

    input_file_path = PathValidator(argv[2], "Input file") \
        .exists() \
        .is_file() \
        .get_path()

    TRADITIONAL = False
    threshold = None

    try:
        threshold = float(argv[3])
    except:
        TRADITIONAL = True


    try:
        color = eval(argv[3])
        r = float(color[0])
    except:
        color = (0, 0, 1)

    (col_r, col_g, col_b) = color
    (col_r, col_g, col_b) = (1 - col_r, 1 - col_g, 1 - col_b)

    output_file_name = output_dir_path.parts[-1].replace(".", "_") + ".png"

    drawHistogram(output_dir_path, input_file_path, output_file_name, TRADITIONAL, threshold, col_r, col_g, col_b, )
