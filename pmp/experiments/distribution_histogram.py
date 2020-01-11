import os
import numpy as np

from PIL import Image, ImageDraw
from math import atan, pi

from .helpers import read_data


class DistributionHistogram:
    def __init__(self, minv, maxv, ppu):
        self.minv = minv
        self.maxv = maxv
        self.ppu = ppu
        self.W = (maxv - minv) * ppu
        self.H = (maxv - minv) * ppu
        self.histogram = [[0] * self.W for _ in range(self.H)]
        self.count = 0

    @staticmethod
    def from_dir(path, minv=-1, maxv=1, ppu=20, winners=True, candidates=False, voters=False):
        voters_h = None
        candidates_h = None
        winners_h = None
        if voters:
            voters_h = DistributionHistogram(minv, maxv, ppu)
        if candidates:
            candidates_h = DistributionHistogram(minv, maxv, ppu)
        if winners:
            winners_h = DistributionHistogram(minv, maxv, ppu)

        for _, _, file_names in os.walk(path):
            for fname in file_names:
                if fname.split('.')[-1] != 'win':
                    continue

                f = open(path + '/' + fname, 'r')
                candidates_list, voters_list, _, winners_list = read_data(f)
                candidates_cords = [(x, y) for _, x, y, _ in candidates_list]

                if voters:
                    voters_h.accumulate_to_hist(voters_list)
                if candidates:
                    candidates_h.accumulate_to_hist(candidates_cords)
                if winners:
                    winners_cords = [candidates_cords[w] for w in winners_list]
                    winners_h.accumulate_to_hist(winners_cords)

        return winners_h, candidates_h, voters_h

    def accumulate_to_hist(self, points):
        for x, y in points:
            x -= self.minv
            y -= self.minv
            x *= self.ppu
            y *= self.ppu
            self.histogram[int(x)][int(y)] += 1
        self.count += 1

    def generate_image(self, path):
        image = Image.new("RGB", (self.W, self.H), "white")
        draw = ImageDraw.Draw(image)

        draw.line((0, self.H / 2, self.W, self.H / 2), fill=128)
        draw.line((self.W / 2, 0, self.W / 2, self.H), fill=128)

        threshold = 0.0005
        total = np.sum(self.histogram)

        for x in range(self.W):
            for y in range(self.H):
                if self.histogram[x][y] > 0:
                    intensity = float(self.histogram[x][y]) / total
                    val = float(intensity) / threshold
                    val = (atan(val)) / (pi / 2)
                    val = 255 - int(val * 255)
                    draw.point((x, (self.H - 1) - y), fill="rgb(%d,%d,%d)" % (val, val, val))

        image.save(path)
