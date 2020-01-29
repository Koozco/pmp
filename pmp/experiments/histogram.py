import numpy as np

from PIL import Image, ImageDraw
from math import atan, pi


class Histogram:
    """Two-dimensional histogram."""

    def __init__(self, minx, maxx, miny, maxy, opacity_mask=(1., 1., 1.), ppu=None, W=256, H=256):
        """
        :param minx: Minimal allowed x value of presented points.
        :type minx: float
        :param maxx: Maximal allowed x value of presented points.
        :type maxx: float
        :param miny: Minimal allowed y value of presented points.
        :type miny: float
        :param maxy: Maximal allowed y value of presented points.
        :type maxy: float
        :param ppu: Points per unit. If provided, width and height are computed based on ppu and min/max x/y.
        :type ppu: int
        :param W: Width of image in pixels. Override by providing ppu.
        :type W: int
        :param H: Height of image in pixels. Override by providing ppu.
        :type H: int
        :param opacity_mask: RGB color mask for drawn histogram cells.
        :type opacity_mask: Tuple[float, float, float]
        """
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.ppu = ppu
        self.W = (maxx - minx) * ppu if ppu is not None else W
        self.H = (maxy - miny) * ppu if ppu is not None else H
        self.count = 0
        self._opacity_mask = opacity_mask
        self._histogram = np.zeros((self.W, self.H), dtype=np.int)
        self._image = Image.new("RGB", (self.W, self.H), "white")
        self._draw = ImageDraw.Draw(self._image)
        self._points_image = Image.new("RGB", (self.W, self.H), "white")
        self._points_image.putalpha(1)
        self._points_draw = ImageDraw.Draw(self._points_image)

    def accumulate(self, points):
        """
        :param points: List of points to be accumulated into histogram.
        :type points: List[Tuple[float, float]]
        """
        for x, y in points:
            if x < self.minx or x > self.maxx or y < self.miny or y > self.maxy:
                continue

            x -= self.minx
            y -= self.miny
            x *= self.ppu
            y *= self.ppu
            self._histogram[int(x)][int(y)] += 1
        self.count += 1

    def draw_fixed_points(self, points, color, size=0):
        """
        :param points: List of points to be draw.
        :type points: List[Tuple[float, float]]
        :param color: RGB color of points.
        :type color: Tuple[int, int, int]
        :param size: Size of points. When equal 0 draw single pixel.
        :type size: int

        Draw fixed points over the main histogram layer.
        """
        if size == 0:
            self._points_draw.point(points, color)
        else:
            for (x, y) in points:
                x0 = max(x - size, 0)
                x1 = min(x + size, self.W)
                y0 = max(y - size, 0)
                y1 = min(y + size, self.H)
                self._points_draw.rectangle((x0, y0, x1, y1), color, color)

    def save_image(self, path):
        """Saves the histogram image. Fixed points are drawn above the histogram itself."""
        self._init_draw()
        self._draw_histogram()
        self._image.paste(self._points_image, mask=self._points_image.split()[3])

        self._image.save(path)

    def _init_draw(self):
        self._draw.line((0, self.H / 2, self.W, self.H / 2), fill=128)
        self._draw.line((self.W / 2, 0, self.W / 2, self.H), fill=128)

    def _draw_histogram(self):
        threshold = 0.0005
        total = np.sum(self._histogram)

        for x in range(self.W):
            for y in range(self.H):
                if self._histogram[x][y] > 0:
                    intensity = float(self._histogram[x][y]) / total
                    val = float(intensity) / threshold
                    val = (atan(val)) / (pi / 2)
                    val = 255 - int(val * 255)
                    color = tuple(int(val * mask) for mask in self._opacity_mask)

                    self._draw.point((x, (self.H - 1) - y), fill="rgb({:d},{:d},{:d})".format(*color))
