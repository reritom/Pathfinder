
from src.plotter import Plotter
import numpy as np
import imageio
import os


plotter = Plotter(50, 50, 20)

map = {
    1: (50, 50, 50, 1),
    2: (100, 100, 100, 1),
    3: (150, 150, 150, 1),
    4: (200, 200, 200, 1),
    5: (50, 100, 150, 1),
    6: (0, 0, 0, 1)
}

points = {}
points[(0, 0)] = 1
points[(1, 1)] = 2
points[(49, 49)] = 3

map_plot = plotter.plot(points, map)
map_plot = plotter.invert(map_plot)

im = np.asarray(map_plot)
imageio.mimsave('./tp.gif', [im], fps=5)
