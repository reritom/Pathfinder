import numpy as np
import math as maths
from itertools import combinations
from .context import Context
from .tools import lies_between, centre_of, is_face_adjacent, Line, LineSet, merge_lines, get_artificial_blocks, surroundings_of
from typing import List
import os, json, copy

class Maze:
    @classmethod
    def from_file(cls, filepath):
        with open(filepath, 'r') as f:
            lines = f.read().splitlines()

        y = len(lines)
        x = len(lines[0])

        instance = cls(x=x, y=y)

        for y_index, line in enumerate(reversed(lines)):
            for x_index, value in enumerate(line):
                if not len(line) == x:
                    raise Exception("Line {} is of len {} while line {} is len {}".format(y_index, len(line), x_index, x))
                if value == 'x':
                    instance.blocks.add((x_index, y_index))

        instance.render_lines()
        """
        for y in range(instance.y):
            for x in range(instance.x):
                if (x, y) in instance.blocks:
                    print('x', end='')
                else:
                    print('-'.format(x), end='')
            print('')
        """

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

        if not self.rendered:
            self.render_lines()

        representation['lines'] = [
            {'a': line.a, 'b': line.b}
            for line in self.lines
        ]

        for x in range(self.x):
            for y in range(self.y):
                if (x, y) not in self.blocks:
                    context = self.get_surroundings((x, y), view_range)
                    representation['positions']["{},{}".format(x, y)] = [surrounding for surrounding in context.surroundings]

        if not 'maze_jsons' in os.listdir('.'):
            os.mkdir('maze_jsons')

        with open(os.path.join('maze_jsons', 'test.json'), 'w') as f:
            f.write(json.dumps(representation))

    def render_lines(self) -> None:
        lines = []

        # Add the border lines
        lines.extend(
            [
                Line((0, 0), (self.x, 0)),
                Line((0, 0), (0, self.y)),
                Line((self.x, 0), (self.x, self.y)),
                Line((0, self.y), (self.x, self.y))
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
        line_set = LineSet()
        line_set.extend(lines)

        #print("Len before getting dupe free {}".format(len(lines)))

        dupe_free = line_set.get_duplicate_free()

        #print("Block count {} line count {}".format(len(self.blocks), len(dupe_free)))
        #print("Dupes {}".format(len(line_set.duplicates)))

        # Now some lines can be merged
        lines = merge_lines(dupe_free)
        self.lines = lines
        self.rendered = True

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

        for line_dict in representation['lines']:
            instance.lines.append[Line(line_dict['a'], line_dict['b'])]
            instance.rendered = True

        instance.pre_rendered = True
        return instance

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.blocks = set()
        self.pre_rendered = False
        self.positions = dict()
        self.rendered = False
        self.lines = []

    def get_full_context(self):
        context = Context()
        context.blocks = self.blocks
        context.surroundings = {
            (x, y)
            for x in range(self.x)
            for y in range(self.y)
            if (x, y) not in self.blocks
        }

        # Strip any that are outside of the grid
        context.clean(self.x, self.y)
        return context

    def get_surroundings(self, position: tuple, view_range: int = 1) -> Context:
        if not self.rendered:
            self.render_lines()

        context = Context()

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
        context.blocks = relevent_blocks

        # In cases of two adjacent faces being blocked, the corner block between them should be considered as a block too
        relevent_blocks = copy.deepcopy(relevent_blocks)
        relevent_blocks = relevent_blocks.union(
            get_artificial_blocks(
                position,
                [surrounding for surrounding in surroundings_of(position) if surrounding in relevent_blocks]
            )
        )

        shadows = set()

        for surrounding in surroundings:
            for block in relevent_blocks:
                if lies_between(block, surrounding, position):
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

        self.rendered = False

    def remove_block(self, block: tuple) -> None:
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
