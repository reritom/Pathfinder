from src.maze import Maze
import numpy as np
import matplotlib
matplotlib.use('TkAgg') # This is to avoid a python macos issue with rendering the canvas
import matplotlib.pyplot as plt
import matplotlib
import imageio

maze = Maze.from_file('example.txt')
print('There are {} blocks total'.format(len(maze.blocks)))

# make a figure + axes
fig, ax = plt.subplots(1, 1, tight_layout=True)
# make color map
my_cmap = matplotlib.colors.ListedColormap(['red', 'green', 'blue', 'black', 'yellow'])
# set the 'bad' values (nan) to be white and transparent
my_cmap.set_bad(color='w', alpha=0)
# draw the grid
N = max([maze.x, maze.y])

for x in range(maze.x):
    for y in range(maze.y):
        ax.axhline(x, lw=0, color='k', zorder=5)
        ax.axvline(y, lw=0, color='k', zorder=5)

images = []

for i in range(0, 20):
    print("Round {}".format(i))
    pos = (i, i)
    context = maze.get_surroundings(pos, 4)

    # make an empty data set
    data = np.ones((maze.x + 1, maze.y + 1)[::-1]) * np.nan

    for surrounding in context.surroundings:
        data[surrounding[::-1]] = 0

    for block in context.blocks:
        data[block[::-1]] = 1

    for block in maze.blocks:
        data[block[::-1]] = 2

    #for perim in context.perimeter:
    #    data[perim] = 3

    data[pos[::-1]] = 3

    print("Starting plot")

    # draw the boxes
    ax.imshow(data, interpolation='none', cmap=my_cmap, extent=[0, maze.x, 0, maze.y], zorder=0)
    # turn off the axis labels
    #ax.axis('off')
    ax.invert_yaxis()

    fig.canvas.draw()       # draw the canvas, cache the renderer
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image  = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    images.append(image)
    print("Finished plot")

imageio.mimsave('./test.gif', images, fps=1)
