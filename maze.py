import numpy as np
from itertools import combinations

class Maze:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.blocks = set()

    def get_surroundings(self, position, view_range=1):
        print("Getting surroundings of {}".format(position))
        # For a given position, return the surrounding positions
        centre_x, centre_y = position

        if view_range == 0:
            return set(position)

        perimeter = self.bresenhams_circle(centre_x, centre_y, view_range)

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

        # Look for any blocks within our surroundings
        relevent_blocks = []
        for block in self.blocks:
            if block in surroundings:
                relevent_blocks.append(block)

        # For each relevent block, determine which of the surroundings it shadows, and those that aren't fully clear
        for block in relevent_blocks:
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
            print(max_theta)

        outmost = []

        #outmost_corner_1 = ?

        # Strip any that are outside of the grid

        class Context:
            def __init__(self):
                self.surroundings = surroundings
                self.blocks = relevent_blocks
                self.obscured = []

        return Context()

    def add_block(self, block: tuple):
        self.blocks.add(block)

    def remove_block(self, x, y):
        pass

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
        boundaries = boundaries.union(clone_octant(centre_x, centre_x, x, y))

        while (y >= x):
            x = x + 1
            if d > 0:
                y = y - 1
                d = d + 4 * (x - y) + 10
            else:
                d = d + 4 * x + 6

            boundaries = boundaries.union(clone_octant(centre_x, centre_x, x, y))

        return boundaries