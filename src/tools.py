from functools import reduce
from typing import List
import math as maths

class Line:
    def __init__(self, a: tuple, b: tuple):
        self.a = a
        self.b = b

    def __repr__(self):
        return str((self.a, self.b))

    def __eq__(self, other):
        return ((self.a == other.a) and (self.b == other.b)) or ((self.a == other.b) and (self.b == other.a))

    def inverse(self):
        return self.__class__(self.b, self.a)

    @property
    def delta(self):
        #print("Getting delta {} {}".format(self.a, self.b))
        dy = self.b[1] - self.a[1]
        dx = self.b[0] - self.a[0]
        return maths.atan2(dy, dx)

    @property
    def dydx(self):
        dy = self.b[1] - self.a[1]
        dx = self.b[0] - self.a[0]
        try:
            return dy/dx
        except:
            return 0

    @property
    def points(self):
        return [self.a, self.b]

def surroundings_of(point: tuple):
    x, y = point
    return [
        (x-1, y-1),
        (x-1, y),
        (x-1, y+1),
        (x, y+1),
        (x, y-1),
        (x+1, y-1),
        (x+1, y),
        (x+1, y+1)
    ]

def line_from_radial(point: tuple, theta, radius):
    dy = maths.sin(theta)*radius
    dx = maths.cos(theta)*radius
    line = Line(point,(dy, dx))
    print("Line from {} {} {}".format(point, theta, radius, line))
    return line

def get_intersection(line_a, line_b):
    """
    Determine the intersection between line_a and line_b, but the intersection is only
    counted if it is between the range of the two line_b points
    """
    #print("Getting intersection of {} {}".format(line_a, line_b))
    # y = mx + c
    a_m = line_a.dydx
    a_c = line_a.a[1] - a_m * line_a.a[0]
    #print("line a {} = {}*{} + {}".format(line_a.a[1], a_m, line_a.a[0], a_c))

    b_m = line_b.dydx
    b_c = line_b.a[1] - b_m * line_b.a[0]
    #print("line a {} = {}*{} + {}".format(line_a.a[1], a_m, line_a.a[0], a_c))

    if a_m == b_m:
        # They are parallel
        #print("They are parellel")
        return "PARALLEL" # todo fix this

    # a_m*x + a_c = b_m*x + b_c
    x_intercept = (b_c - a_c) / (a_m - b_m)
    y_intercept = a_m*x_intercept + a_c

    # Check if the intercepts are within the line_a segment
    max_x = max(line_a.a[0], line_a.b[0])
    min_x = min(line_a.a[0], line_a.b[0])
    max_y = max(line_a.a[1], line_a.b[1])
    min_y = min(line_a.a[1], line_a.b[1])

    if (x_intercept >= min_x) and (x_intercept <= max_x) and (y_intercept >= min_y) and (y_intercept <= max_y):

        # Check if the intercepts are within the line_b segment
        max_x = max(line_b.a[0], line_b.b[0])
        min_x = min(line_b.a[0], line_b.b[0])
        max_y = max(line_b.a[1], line_b.b[1])
        min_y = min(line_b.a[1], line_b.b[1])

        if (x_intercept >= min_x) and (x_intercept <= max_x) and (y_intercept >= min_y) and (y_intercept <= max_y):
            #print("intercept ok")
            return (x_intercept, y_intercept)

    # Intercept doesn't lie on the segment
    #print("{} Intercept is out of range".format((x_intercept, y_intercept)))
    return False

def get_magnitude(line: Line):
    dy = abs(line.a[1] - line.b[1])
    dx = abs(line.a[0] - line.b[0])
    return maths.sqrt(dy**2 + dx**2)

def merge_lines(lines: List[Line]) -> list:
    def recurse(lines_to_merge):
        lines_copy = [l for l in lines_to_merge]

        for index, line in enumerate(lines_copy):
            surrounding_lines = [
                l
                for l in lines_copy
                if l != line
                and (
                    l.a == line.a
                    or l.b == line.b
                    or l.a == line.b
                    or l.b == line.a
                )
            ]

            for surrounding_line in surrounding_lines:
                if surrounding_line.delta == line.delta:
                    #print("Merging lines {} and {}".format(surrounding_line, line))
                    # These two lines share a point, the point they share will be merged
                    shared_point = line.a if line.a in surrounding_line.points else line.b
                    new_point_a = next(filter(lambda p: p != shared_point, line.points))
                    new_point_b = next(filter(lambda p: p != shared_point, surrounding_line.points))
                    new_line = Line(new_point_a, new_point_b)

                    # Remove the line and the surrounding line from the lines
                    lines_copy.remove(line)
                    lines_copy.remove(surrounding_line)

                    # Add the new line
                    lines_copy.append(new_line)
                    return recurse(lines_copy)

        else:
            return lines_copy

    return recurse(lines)

def remove_duplicates(lines: List[Line]):
    pass

class LineSet:
    def __init__(self, remove_duplicates=False):
        self.remove_duplicates = remove_duplicates
        self.lines = []
        self.duplicates = []

    def get_duplicate_free(self):
        lines = [line for line in self.lines]

        for dupe in self.duplicates:
            while True:
                try:
                    lines.remove(dupe)
                except ValueError:
                    break

            while True:
                try:
                    lines.remove(dupe.inverse())
                except ValueError:
                    break

        return lines

    def __contains__(self, line: Line) -> bool:
        return line in self.lines

    def add(self, line: Line) -> None:
        if self.remove_duplicates:
            if line not in self:
                self.lines.append(line)
        else:
            if line in self:
                self.duplicates.append(line)

            self.lines.append(line)

    def extend(self, lines: List[Line]) -> None:
        for line in lines:
            self.add(line)

    def __len__(self) -> int:
        return len(self.lines)

def centre_of(block: tuple) -> tuple:
    return (block[0] + 0.5, block[1] + 0.5)

def corners_of(block: tuple) -> list:
    return [
        block,
        (block[0] + 1, block[1]),
        (block[0], block[1] + 1),
        (block[0] + 1, block[1] + 1)
    ]

def edges_of(block: tuple) -> List[Line]:
    return [
        Line((block[0], block[1]), (block[0] + 1, block[1])),
        Line((block[0], block[1]), (block[0], block[1] + 1)),
        Line((block[0] + 1, block[1] + 1), (block[0], block[1] + 1)),
        Line((block[0] + 1, block[1] + 1), (block[0] + 1, block[1]))
    ]

def is_adjacent(block_a: tuple, block_b: tuple) -> bool:
    corners_of_a = corners_of(block_a)
    corners_of_b = corners_of(block_b)

    for corner in corners_of_a:
        if corner in corners_of_b:
            return True

def is_face_adjacent(block_a: tuple, block_b: tuple) -> bool:
    corners_of_a = corners_of(block_a)
    corners_of_b = corners_of(block_b)
    corners_touching = 0

    for corner in corners_of_a:
        if corner in corners_of_b:
            corners_touching += 1

    return True if corners_touching == 2 else False

def is_corner_adjacent(block_a: tuple, block_b: tuple) -> bool:
    corners_of_a = corners_of(block_a)
    corners_of_b = corners_of(block_b)
    corners_touching = 0

    for corner in corners_of_a:
        if corner in corners_of_b:
            corners_touching += 1

    return True if corners_touching == 1 else False

def lies_between(obstacle: tuple, point_a: tuple, point_b: tuple) -> bool:
    a_b_line = Line(point_a, point_b)
    obstacle_lines = edges_of(obstacle)

    for obstacle_line in obstacle_lines:
        #print("Finding intercept between {} and {}".format(a_b_line, obstacle_line))
        intersect = get_intersection(a_b_line, obstacle_line)
        #print("Intersection at {}".format(intersect))
        if intersect == 'PARALLEL':
            mag_a_b = get_magnitude(a_b_line)
            mag_a_o = get_magnitude(Line(point_a, centre_of(obstacle)))
            mag_b_o = get_magnitude(Line(point_b, centre_of(obstacle)))
            evaluation = abs(mag_a_b - (mag_a_o + mag_b_o))
            #print("Evaluation is {}".format(evaluation))
            evaluation = evaluation <= 0.1
            if evaluation:
                #print("Parellel block")
                return True

        elif intersect:
            return True

def get_artificial_blocks(point, surrounding_blocks):
    x, y = point

    face_pairs = [
        [
            Line((x, y), (x+1, y)),
            Line((x, y), (x, y+1)),
            (x-1, y-1)
        ],
        [
            Line((x+1, y), (x, y)),
            Line((x+1, y), (x, y+1)),
            (x+1, y-1)
        ],
        [
            Line((x, y+1), (x+1, y)),
            Line((x, y+1), (x, y)),
            (x-1, y+1)
        ],
        [
            Line((x+1, y+1), (x+1, y)),
            Line((x+1, y+1), (x, y+1)),
            (x+1, y+1)
        ]
    ]

    edges = []
    for surrounding_block in surrounding_blocks:
        edges.extend(edges_of(surrounding_block))

    artificial_blocks = []
    for face_pair in face_pairs:
        if face_pair[0] in edges and face_pair[1] in edges:
            artificial_blocks.append(face_pair[2])

    print("There are {} artifical blocks".format(len(artificial_blocks)))
    return artificial_blocks
