import numpy as np
import math as maths
from itertools import combinations
from .context import Context

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

        return instance

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.blocks = set()

    def get_surroundings(self, position, view_range=1):
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

        # For each relevent block, determine which of the surroundings it shadows, and those that aren't fully clear
        print("There are {} relevent blocks".format(len(relevent_blocks)))
        for index, block in enumerate(relevent_blocks):
            #print("Looking at block {}".format(index))
            # From the centre, looks for the intercept of the corners of the block
            corners = [
                np.array([block[0], block[1]]),
                np.array([block[0] + 1, block[1]]),
                np.array([block[0], block[1] + 1]),
                np.array([block[0] + 1, block[1] + 1])
            ]

            centre = np.array([centre_x + 0.5, centre_y + 0.5])

            # List of different combinations of two corners
            mixes = combinations(corners, 2)

            # Find the greatest angle between two corners
            theta_results = []

            for combo in mixes:
                corner_1 = combo[0]
                corner_2 = combo[1]

                # Normalise the two points relative to the centre
                c1_centre = corner_1 - centre
                c2_centre = corner_2 - centre

                cosine_angle = np.dot(c1_centre, c2_centre) / (np.linalg.norm(c1_centre) * np.linalg.norm(c2_centre))
                angle = np.arccos(cosine_angle)
                theta_results.append((angle, corner_1, corner_2))

            greatest_combo = max(theta_results, key = lambda result: result[0])
            max_theta = greatest_combo[0]
            #print("Max theta {}".format(max_theta))
            #print("Range {}".format(max_theta/(maths.pi*2*view_range*2)*1000000))

            theta_to_corner_1 = self.angle_between(position, greatest_combo[1])
            theta_to_corner_2 = self.angle_between(position, greatest_combo[2])
            #print("Theta to corner 1 {}".format(theta_to_corner_1))
            #print("Theta to corner 2 {}".format(theta_to_corner_2))

            # These arent needed but look nice on the plots
            c1_outmost = (int(np.cos(theta_to_corner_1)*view_range) + position[0], int(np.sin(theta_to_corner_1)*view_range) + position[1])
            c2_outmost = (int(np.cos(theta_to_corner_2)*view_range) + position[0], int(np.sin(theta_to_corner_2)*view_range) + position[1])

            context.outmost.add(c1_outmost)
            context.outmost.add(c2_outmost)

            # We need to ensure the next iteration range goes from min the max
            min_corner_theta = min([theta_to_corner_1, theta_to_corner_2])
            max_corner_theta = max([theta_to_corner_1, theta_to_corner_2])

            theta_range = range(int(min_corner_theta*1_000_000), int(max_corner_theta*1_000_000), int((max_theta/(maths.pi*2*view_range*2))*1_000_000))

            for theta_times_1000000 in theta_range:
                for double_radius in range(2*(view_range + 1)):
                    radius = double_radius / 2
                    theta = theta_times_1000000 / 1_000_000
                    point = (maths.floor(np.cos(theta)*radius) + block[0], maths.floor(np.sin(theta)*radius) + block[1])
                    context.shadows.add(point)

        print("Length of shadows {}".format(len(context.shadows)))

        # Strip any that are outside of the grid
        context.clean(self.x, self.y)
        print("Length of shadows after clean {}".format(len(context.shadows)))
        print('Length of surroundings after clean {}'.format(len(context.surroundings)))

        return context

    def add_block(self, block: tuple):
        if block[0] > 0 and block[0] < self.x:
            if block[1] > 0 and block[1] < self.y:
                self.blocks.add(block)

    def remove_block(self, block: tuple):
        self.blocks.discard(block)

    @staticmethod
    def angle_between(p1, p2):
        theta = np.arctan2(p2[1] - p1[1], p2[0] - p1[0])
        return theta

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
