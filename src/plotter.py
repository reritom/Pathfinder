from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import math as maths

heatmap = { # TODO convert this to an algorithm
    0.00: (216, 50, 45),
    0.05: (220, 70, 48),
    0.10: (228, 90, 51),
    0.15: (233, 115, 55),
    0.20: (238, 139, 59),
    0.25: (241, 158, 63),
    0.30: (245, 177, 66),
    0.35: (247, 197, 80),
    0.40: (250, 217, 98),
    0.45: (252, 232, 119),
    0.50: (254, 250, 137),
    0.55: (200, 245, 146),
    0.60: (164, 238, 154),
    0.65: (130, 228, 164),
    0.70: (98, 219, 175),
    0.75: (89, 200, 185),
    0.80: (80, 188, 195),
    0.85: (70, 173, 197),
    0.90: (61.9, 158, 198),
    0.95: (51.9, 135, 190),
    1.00: (44.1, 124.3, 183.5)
}

def get_pixel(value, map):
    valued = round(value / 0.05) * 0.05
    valued = round(valued, 2)
    return map[valued]

class Plotter:
    def __init__(self, x, y, spacing):
        self.spacing = spacing
        self.grid = self._draw_grid(x, y, spacing)
        self.x = x
        self.y = y

    def invert(self, plot):
        return plot.transpose(Image.FLIP_TOP_BOTTOM)

    def _draw_grid(self, x, y, spacing):
        grid = Image.new('RGBA', (x*spacing, y*spacing), (250, 250, 250, 1))
        drawer = ImageDraw.Draw(grid)

        for xv in range(x):
            drawer.line([(xv*spacing, 0), (xv*spacing, y*spacing)], fill=(200, 200, 200, 1), width=1)

        for yv in range(y):
            drawer.line([(0, yv*spacing), (x*spacing, yv*spacing)], fill=(200, 200, 200, 1), width=1)

        return grid

    def plot(self, points, map: dict, plot: Image = None, inverse=False):
        if not plot:
            plot = self.grid.copy()

        drawer = ImageDraw.Draw(plot)

        for point, value in points.items():
            px, py = point
            drawer.rectangle(
                [
                    (px*self.spacing, py*self.spacing),
                    ((px + 1)*self.spacing - 1, (py + 1)*self.spacing - 1)
                ],
                fill=map[value],
                outline=map[value]
            )

        if inverse:
            return plot.transpose(Image.FLIP_TOP_BOTTOM)
        else:
            return plot

    def plot_lines(self, plot, lines: list, colour: tuple, inverse=False):
        #print("Drawing {} lines".format(len(lines)))
        drawer = ImageDraw.Draw(plot)

        for line in lines:
            # Scale the line
            line = (
                (line[0][0]*self.spacing, line[0][1]*self.spacing),
                (line[1][0]*self.spacing, line[1][1]*self.spacing)
            )

            drawer.line(
                line,
                fill=colour,
                width=1
            )

        if inverse:
            return plot.transpose(Image.FLIP_TOP_BOTTOM)
        else:
            return plot

    def plot_heatmap(self, points: dict, inverse=False, blur=True, max_val=None, min_val=None, extra_mapping=None):
        if blur:
            plot = Image.new('RGBA', (self.x*self.spacing, self.y*self.spacing), (250, 250, 250, 1))
        else:
            plot = self.grid.copy()

        drawer = ImageDraw.Draw(plot)
        #print("Drawing points {}".format(len(points)))

        if not (max_val and min_val):
            # Determine the range
            max_val, min_val = None, None
            for point, value in points.items():
                # Skip any of the extra mappings
                if extra_mapping and value in extra_mapping:
                    continue
                if min_val is None:
                    min_val = value
                if max_val is None:
                    max_val = value

                max_val = max([max_val, value])
                min_val = min([min_val, value])

        def mapper(value, min_val, max_val):
            mapped = (value - min_val)/(max_val - min_val)
            return mapped

        for point, value in points.items():
            px, py = point
            pixel_float = (
                extra_mapping[value]
                if extra_mapping
                and value in extra_mapping
                else mapper(value, min_val, max_val)
            )

            r, g, b = get_pixel(pixel_float, heatmap)
            r, g, b = int(r), int(g), int(b)

            drawer.rectangle(
                [
                    (px*self.spacing, py*self.spacing),
                    ((px + 1)*self.spacing - 1, (py + 1)*self.spacing - 1)
                ],
                fill=(r, g, b, 1),
                outline=(r, g, b, 1)
            )

        if blur:
            plot = plot.filter(ImageFilter.GaussianBlur(self.spacing/3))

        if inverse:
            return plot.transpose(Image.FLIP_TOP_BOTTOM)
        else:
            return plot

if __name__=='__main__':
    plotter = Plotter(40, 40, 30)
    grid = plotter.grid
    grid.save("testim.bmp")
