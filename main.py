from maze import Maze
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import imageio

N = 100
maze = Maze(N, N)
maze.add_block((int(N/2)+5, int(N/2)+5))
images = []

for i in range(0, 10):
    context = maze.get_surroundings((int(N/2) + i, int(N/2) + i), 30)
    surroundings = context.surroundings

    # make an empty data set
    data = np.ones((N, N)) * np.nan

    for surrounding in surroundings:
        data[surrounding] = 1

    for block in context.blocks:
        data[block] = 2

    # make a figure + axes
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    # make color map
    my_cmap = matplotlib.colors.ListedColormap(['r', 'g', 'b'])
    # set the 'bad' values (nan) to be white and transparent
    my_cmap.set_bad(color='w', alpha=0)
    # draw the grid
    for x in range(N + 1):
        ax.axhline(x, lw=0, color='k', zorder=5)
        ax.axvline(x, lw=0, color='k', zorder=5)
    # draw the boxes
    ax.imshow(data, interpolation='none', cmap=my_cmap, extent=[0, N, 0, N], zorder=0)
    # turn off the axis labels
    ax.axis('off')

    fig.canvas.draw()       # draw the canvas, cache the renderer
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image  = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    images.append(image)

imageio.mimsave('./test.gif', images, fps=1)