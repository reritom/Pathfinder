from src.maze import Maze
from src.bot import Bot
from src.plotter import Plotter
import numpy as np
import imageio
import os, copy


maze = Maze.from_file(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'mazes',
        'complex.txt'
    )
)

#print("Rendering")
#maze.render_to_json(5)
#print("Finished rendering")
"""

print("Loading maze from json")
maze = Maze.from_json(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'maze_jsons',
        'test.json'
    )
)

maze = Maze(50,50)

print('There are {} blocks total'.format(len(maze.blocks)))
"""
plotter = Plotter(maze.x, maze.y, 10)
#plotter.set_null('black')

map = {
    1: (50, 50, 50, 1),
    2: (100, 100, 100, 1),
    3: (150, 150, 150, 1),
    4: (200, 200, 200, 1),
    5: (50, 100, 150, 1),
    6: (0, 0, 0, 1),
    7: (255, 243, 122, 1)
}

images_mp = []
images_sp = []
images_dp = []

bot = Bot(
    position=(0, 0),
    destination=(40, 40)
)

for i in range(0, 400):
    if bot.position == bot.destination:
        break

    print("Round {}".format(i))

    """
    if i == 0:
        context = maze.get_full_context()
    else:
        context = maze.get_surroundings(bot.position, 5)
    """
    context = maze.get_surroundings(bot.position, 5)
    bot.run_round(context)
    static_points = bot.get_static_heuristics()
    dynamic_points = bot.get_dynamic_heuristics()

    # ------- Basic plot ----

    points = {}

    for block in context.blocks:
        points[block] = 2

    for block in maze.blocks:
        points[block] = 3

    for surrounding in context.surroundings:
        points[surrounding] = 4

    points[bot.ltaf] = 1
    points[bot.position] = 2
    points[(40, 40)] = 5

    if bot.waypoint:
        for location in bot.waypoint:
            points[location] = 7

    map_plot = plotter.plot(points, map)

    # -------- Static plot -------
    static_plot = plotter.plot_heatmap(static_points)#, max_val=max_val, min_val=min_val)

    # Plot empty blocks to ease the blur
    static_plot = plotter.plot(
        {block: 1 for block in maze.blocks},
        {1: (250, 250, 250, 1)},
        static_plot
    )

    # Plot each of the non-static points also to ease the blur
    static_plot = plotter.plot(
        {(x, y): 1 for x in range(maze.x) for y in range(maze.y) if (x, y) not in static_points},
        {1: (250, 250, 250, 1)},
        static_plot
    )

    # Plot the bot and target
    static_plot = plotter.plot(
        {bot.position: 1, bot.target: 1},
        {1: (220, 220, 220, 1)},
        static_plot
    )

    # Plot the outlines of the blocks
    static_plot = plotter.plot_lines(
        static_plot,
        [(line.a, line.b) for line in maze.lines],
        (200, 200, 200, 1)
    )


    # ------- Dynamic plot -----
    # Some dynamic points are None, meaning they should be considered as lowest temperature without skewing the scales
    dynamic_plot = plotter.plot_heatmap(dynamic_points, extra_mapping={None: 0})#, max_val=max_val, min_val=min_val)

    # Plot empty blocks to ease the blur
    dynamic_plot = plotter.plot(
        {block: 1 for block in maze.blocks},
        {1: (250, 250, 250, 1)},
        dynamic_plot
    )

    # Plot each of the non-dynamic points also to ease the blur
    dynamic_plot = plotter.plot(
        {(x, y): 1 for x in range(maze.x) for y in range(maze.y) if (x, y) not in dynamic_points},
        {1: (250, 250, 250, 1)},
        dynamic_plot
    )

    # Plot the bot and target
    dynamic_plot = plotter.plot(
        {bot.position: 1, bot.target: 1},
        {1: (220, 220, 220, 1)},
        dynamic_plot
    )

    # Plot the outlines of the blocks
    dynamic_plot = plotter.plot_lines(
        dynamic_plot,
        [(line.a, line.b) for line in maze.lines],
        (200, 200, 200, 1)
    )

    images_mp.append(np.asarray(plotter.invert(map_plot)))
    images_sp.append(np.asarray(plotter.invert(static_plot)))
    images_dp.append(np.asarray(plotter.invert(dynamic_plot)))

imageio.mimsave('./test_mp.gif', images_mp, fps=10)
imageio.mimsave('./test_sp.gif', images_sp, fps=10)
imageio.mimsave('./test_dp.gif', images_dp, fps=10)
