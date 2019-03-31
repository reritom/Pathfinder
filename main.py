from src.maze import Maze
from src.bot import Bot
import numpy as np
import matplotlib
matplotlib.use('TkAgg') # This is to avoid a python macos issue with rendering the canvas
import matplotlib.pyplot as plt
import matplotlib
import imageio
import os
from src.plotter import Plotter

"""
maze = Maze.from_file(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'mazes',
        'complex.txt'
    )
)

print("Rendering")
maze.render_to_json(4)
print("Finished rendering")
"""

print("Loading maze from json")
maze = Maze.from_json(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'maze_jsons',
        'test.json'
    )
)


print('There are {} blocks total'.format(len(maze.blocks)))

plotter = Plotter(maze.x, maze.y, 20)
#plotter.set_null('black')

map = {
    1: (50, 50, 50, 1),
    2: (100, 100, 100, 1),
    3: (150, 150, 150, 1),
    4: (200, 200, 200, 1)
}

images_mp = []
images_sp = []

bot = Bot((0, 0), (30, 30))

for i in range(0, 20):
    print("Round {}".format(i))
    pos = (i, i)
    context = maze.get_surroundings(pos, 4)
    bot.run_round(context.surroundings)
    static_points = bot.get_static_heuristics()
    #dynamic_points = bot.get_dynamic_heuristics()


    points = {}

    for block in context.blocks:
        points[block] = 1

    for block in maze.blocks:
        points[block] = 2

    for surrounding in context.surroundings:
        points[surrounding] = 3

    points[pos] = 4

    map_plot = plotter.plot(points, map)

    static_plot = plotter.plot_heatmap(static_points)
    static_plot = plotter.plot(
        {block: 1 for block in maze.blocks},
        {1: (200, 200, 200, 1)},
        static_plot
    )

    images_mp.append(np.asarray(map_plot))
    images_sp.append(np.asarray(static_plot))
    print("Finished plot")

imageio.mimsave('./test_mp.gif', images_mp, fps=1)
imageio.mimsave('./test_sp.gif', images_sp, fps=1)
