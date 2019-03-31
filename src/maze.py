import numpy as np
import math as maths
from itertools import combinations
from .context import Context
from .tools import lies_between, centre_of, is_adjacent
from typing import List
import os, json

class Maze:
    @classmethod
    def from_file(cls, filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()

        y = len(lines)
        x = len(lines[0])

        instance = cls(x=x, y=y)

        for y_index, line in enumerate(lines):
            for x_index, value in enumerate(line):
                if value == 'x':
                    instance.blocks.add((x_index, y-y_index))

        return instance

    def render_to_json(self, view_range: int):
        """
        Process the maze and available positions for any given point for a given range
        and store it as a json representation
        """
        representation = {
            'dimensions': {
                'x': self.x,
                'y': self.y
            },
            'range': view_range,
            'blocks': [block for block in self.blocks],
            'positions': {}
        }

        for x in range(self.x):
            for y in range(self.y):
                if (x, y) not in self.blocks:
                    context = self.get_surroundings((x, y), view_range)
                    representation['positions']["{},{}".format(x, y)] = [surrounding for surrounding in context.surroundings]

        if not 'maze_jsons' in os.listdir('.'):
            os.mkdir('maze_jsons')

        with open(os.path.join('maze_jsons', 'test.json'), 'w') as f:
            f.write(json.dumps(representation))

    @classmethod
    def from_json(cls, filepath: str):
        with open(filepath, 'r') as f:
            representation = json.load(f)

        instance = cls(representation['dimensions']['x'], representation['dimensions']['y'])
        instance.blocks = set([(block[0], block[1]) for block in representation['blocks']])

        for key, value in representation['positions'].items():
            split = key.split(',')
            position_tuple = (int(split[0]), int(split[1]))
            surroundings = set([(surrounding[0], surrounding[1]) for surrounding in value])
            instance.positions[position_tuple] = surroundings

        instance.pre_rendered = True
        return instance

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.blocks = set()
        self.pre_rendered = False
        self.positions = dict()

    def get_surroundings(self, position: tuple, view_range: int = 1) -> Context:
        context = Context()
        context.blocks = self.blocks

        # For a given position, return the surrounding positions
        centre_x, centre_y = position

        if view_range == 0 or position in self.blocks:
            return context

        if self.pre_rendered:
            context.surroundings = self.positions[position]
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
        #print('Surroundings are {}'.format(len(context.surroundings)))

        relevent_blocks = {block for block in self.blocks if block in surroundings}
        shadows = set()

        for surrounding in surroundings:
            for block in relevent_blocks:
                if not is_adjacent(block, position):
                    if lies_between(centre_of(block), centre_of(surrounding), centre_of(position)):
                        shadows.add(surrounding)

        for shadow in shadows:
            context.surroundings.discard(shadow)

        # Strip any that are outside of the grid
        context.clean(self.x, self.y)

        return context

    def add_block(self, block: tuple) -> None:
        if block[0] > 0 and block[0] < self.x:
            if block[1] > 0 and block[1] < self.y:
                self.blocks.add(block)

    def remove_block(self, block: tuple) -> None:
        self.blocks.discard(block)

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
