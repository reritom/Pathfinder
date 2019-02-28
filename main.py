from maze import Maze
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

N = 100
maze = Maze(N, N)
maze.add_block((int(N/2)+5, int(N/2)+5))
surroundings = maze.get_surroundings((int(N/2), int(N/2)), 30)
#print(surroundings)
print(maze.blocks)


# make an empty data set
data = np.ones((N, N)) * np.nan
# fill in some fake data
#for j in range(3)[::-1]:
#    data[N//2 - j : N//2 + j +1, N//2 - j : N//2 + j +1] = j

for surrounding in surroundings:
    data[surrounding] = 1
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
plt.show()