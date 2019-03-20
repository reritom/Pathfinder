import numpy as np
import math as maths
from itertools import combinations
from .context import Context
from .tools import LineSet, Line

class Maze:
    @classmethod
    def from_file(cls, filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()

        y = len(lines)
        x = len(lines[0])

        print("Maze x {}".format(x))
        print("Maze y {}".format(y))


        instance = cls(x=x, y=y)

        for y_index, line in enumerate(lines):
            for x_index, value in enumerate(line):
                if value == 'x':
                    instance.blocks.add((x_index, y-y_index))

        instance.render_lines()
        return instance

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rendered = False
        self.blocks = set()
        self.lines = LineSet()

    def render_lines(self):
        lines = []

        # Add the border lines
        lines.extend(
            [
                Line((0, 0), (self.x+1, 0)),
                Line((0, 0), (0, self.y+1)),
                Line((self.x+1, 0), (self.x+1, self.y+1)),
                Line((0, self.y+1), (self.x+1, self.y+1))
            ]
        )

        # Add the lines surrounding blocks
        for block in self.blocks:
            x, y = block

            lines.extend(
                [
                    Line((x, y), (x, y+1)),
                    Line((x, y), (x+1, y)),
                    Line((x+1, y), (x+1, y+1)),
                    Line((x, y+1), (x+1, y+1))
                ]
            )

        # Add the lines to the list
        self.lines.extend(lines)

        dupe_free = self.lines.get_duplicate_free()

        print("Block count {} line count {}".format(len(self.blocks), len(dupe_free)))
        print("Dupes {}".format(len(self.lines.duplicates)))
        self.rendered = True

    def get_surroundings(self, position, view_range=1):
        if not self.rendered:
            raise Exception("Maze needs rendering prior to retrieving surroundings")

        context = Context()

        # For a given position, return the surrounding positions
        centre_x, centre_y = position

        if view_range == 0 or position in self.blocks:
            return context

        perimeter = self.bresenhams_circle(centre_x, centre_y, view_range)
        context.perimeter = context.perimeter.union(perimeter)

        # We will fill the area within the perimeter
        surroundings = set().union(perimeter)

        for x in range(centre_x - view_range, centre_x + view_range):
            # Find any perimeter points for this x value
            perimeter_points = list(filter(lambda this_point: this_point[0] == x, perimeter))

            if len(perimeter_points) == 1:
                pass
            elif len(perimeter_points) > 1:
                # We will fill all the points between the two/four perimeter points
                max_y = max([point[1] for point in perimeter_points])
                min_y = min([point[1] for point in perimeter_points])

                for y in range(min_y, max_y):
                    surroundings.add((x, y))
            else:
                pass

        # Add the filled surroundings to the context
        context.surroundings = context.surroundings.union(surroundings)
        print('Surroundings are {}'.format(len(context.surroundings)))

        # Look for any blocks within our surroundings
        relevent_blocks = []
        for block in self.blocks:
            if block in surroundings:
                relevent_blocks.append(block)

        context.blocks = context.blocks.union(relevent_blocks)

        # Strip any that are outside of the grid
        context.clean(self.x, self.y)

        return context

    def add_block(self, block: tuple):
        if block[0] > 0 and block[0] < self.x:
            if block[1] > 0 and block[1] < self.y:
                self.blocks.add(block)

        self.rendered = False

    def remove_block(self, block: tuple):
        self.blocks.discard(block)
        self.rendered = False

    def bresenhams_circle(self, centre_x: int, centre_y: int, radius: int) -> list:
        def clone_octant(centre_x, centre_y, x, y):
            return [
                (centre_x + x, centre_y + y),
                (centre_x - x, centre_y + y),
                (centre_x + x, centre_y - y),
                (centre_x - x, centre_y - y),
                (centre_x + y, centre_y + x),
                (centre_x - y, centre_y + x),
                (centre_x + y, centre_y - x),
                (centre_x - y, centre_y - x),
            ]

        x = 0
        y = radius
        d = 3 - 2 * radius
        boundaries = set()
        boundaries = boundaries.union(clone_octant(centre_x, centre_y, x, y))

        while (y >= x):
            x = x + 1
            if d > 0:
                y = y - 1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6

            boundaries = boundaries.union(clone_octant(centre_x, centre_y, x, y))

        return boundaries