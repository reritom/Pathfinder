from src.maze import Maze
from src.bot import Bot
from src.plotter import Plotter
import numpy as np
import imageio
import os

"""
maze = Maze.from_file(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'mazes',
        'complex.txt'
    )
)

print("Rendering")
maze.render_to_json(6)
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
    4: (200, 200, 200, 1),
    5: (50, 100, 150, 1)
}

images_mp = []
images_sp = []
images_dp = []

bot = Bot((0, 0), (40, 40))

for i in range(0, 40):
    print("Round {}".format(i))
    pos = (i, i)
    context = maze.get_surroundings(pos, 7)
    bot.run_round(context)
    static_points = bot.get_static_heuristics()
    dynamic_points = bot.get_dynamic_heuristics()

    # Determine the max and min points collectively for the heatmaps to share the same range
    max_val, min_val = None, None
    for point, value in static_points.items():
        if min_val is None:
            min_val = value
        if max_val is None:
            max_val = value

        max_val = max([max_val, value])
        min_val = min([min_val, value])

    for point, value in dynamic_points.items():
        if min_val is None:
            min_val = value
        if max_val is None:
            max_val = value

        max_val = max([max_val, value])
        min_val = min([min_val, value])

    # ------- Basic plot ----


    points = {}

    for block in context.blocks:
        points[block] = 1

    for block in maze.blocks:
        points[block] = 2

    for surrounding in context.surroundings:
        points[surrounding] = 3

    points[pos] = 4
    points[(40, 40)] = 5

    map_plot = plotter.plot(points, map)

    # -------- Static plot -------

    print("Plotting static heatmap")
    static_plot = plotter.plot_heatmap(static_points)#, max_val=max_val, min_val=min_val)

    static_plot = plotter.plot(
        {block: 1 for block in maze.blocks},
        {1: (250, 250, 250, 1)},
        static_plot
    )

    static_plot = plotter.plot(
        {(x, y): 1 for x in range(maze.x) for y in range(maze.y) if (x, y) not in static_points},
        {1: (250, 250, 250, 1)},
        static_plot
    )

    static_plot = plotter.plot_lines(
        static_plot,
        [(line.a, line.b) for line in maze.lines],
        (200, 200, 200, 1)
    )

    # ------- Dynamic plot -----
    print("Plotting dynamic heatmap")
    dynamic_plot = plotter.plot_heatmap(dynamic_points)#, max_val=max_val, min_val=min_val)

    dynamic_plot = plotter.plot(
        {block: 1 for block in maze.blocks},
        {1: (250, 250, 250, 1)},
        dynamic_plot
    )

    dynamic_plot = plotter.plot(
        {(x, y): 1 for x in range(maze.x) for y in range(maze.y) if (x, y) not in dynamic_points},
        {1: (250, 250, 250, 1)},
        dynamic_plot
    )

    dynamic_plot = plotter.plot_lines(
        dynamic_plot,
        [(line.a, line.b) for line in maze.lines],
        (200, 200, 200, 1)
    )

    images_mp.append(np.asarray(map_plot))
    images_sp.append(np.asarray(static_plot))
    images_dp.append(np.asarray(dynamic_plot))
    print("Finished plot")

imageio.mimsave('./test_mp.gif', images_mp, fps=3)
imageio.mimsave('./test_sp.gif', images_sp, fps=3)
imageio.mimsave('./test_dp.gif', images_dp, fps=3)
