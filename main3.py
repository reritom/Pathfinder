from src.maze import Maze
from src.tools import Line

# Create a rectangle shape as such with segments of 1 unit length
lines_to_merge = [
    Line((0, 0), (0, 1)),
    Line((0, 1), (1, 1)),
    Line((1, 1), (2, 1)),
    Line((2, 1), (2, 0)),
    Line((2, 0), (1, 0)),
    Line((1, 0), (0, 0))
]

# When we merge, we expect the two longer sides to merge from 2 lines each, to 1 line each
merged = Maze.merge_lines(lines_to_merge)

print(merged)
