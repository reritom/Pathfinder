from typing import List, Tuple
from PIL import Image, ImageDraw
import numpy as np


class Plotter:
    def __init__(self, x, y, spacing):
        self.spacing = spacing
        self.grid = self._draw_grid(x, y, spacing)
        self.x = x
        self.y = y

    def _draw_grid(self, x, y, spacing):
        grid = Image.new('RGBA', (x*spacing, y*spacing), (250, 250, 250, 1))
        drawer = ImageDraw.Draw(grid)

        for xv in range(x):
            drawer.line([(xv*spacing, 0), (xv*spacing, y*spacing)], fill=(200, 200, 200, 1), width=1)

        for yv in range(y):
            drawer.line([(0, yv*spacing), (x*spacing, yv*spacing)], fill=(200, 200, 200, 1), width=1)

        return grid

    def plot(self, points, map: dict, plot: Image = None, inverse=True):
        if not plot:
            plot = self.grid.copy()

        drawer = ImageDraw.Draw(plot)

        for point, value in points.items():
            if inverse:
                point = (point[0], self.y - point[1])

            drawer.rectangle(
                [
                    (point[0]*self.spacing, point[1]*self.spacing),
                    ((point[0] + 1)*self.spacing, (point[1] + 1)*self.spacing)
                ],
                fill=map[value],
                outline=(0,0,255,255)
            )

        return plot

    def plot_heatmap(self, points: dict, range: tuple = 1, inverse=True):
        plot = self.grid.copy()
        drawer = ImageDraw.Draw(plot)
        print("Drawing points {}".format(len(points)))

        for point, value in points.items():
            if inverse:
                point = (point[0], self.y - point[1])

            drawer.rectangle(
                [
                    (point[0]*self.spacing, point[1]*self.spacing),
                    ((point[0] + 1)*self.spacing, (point[1] + 1)*self.spacing)
                ],
                fill=(0, 0, 0, 1),
                outline=(0,0,255,255)
            )

        return plot


if __name__=='__main__':
    plotter = Plotter(40, 40, 30)
    grid = plotter.grid
    grid.save("testim.bmp")
