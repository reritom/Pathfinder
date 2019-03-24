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
    print("Getting intersection of {} {}".format(line_a, line_b))
    # y = mx + c
    a_m = line_a.dydx
    a_c = line_a.a[1] - a_m * line_a.a[0]
    #print("line a {} = {}*{} + {}".format(line_a.a[1], a_m, line_a.a[0], a_c))

    b_m = line_b.dydx
    b_c = line_b.a[1] - b_m * line_b.a[0]
    #print("line a {} = {}*{} + {}".format(line_a.a[1], a_m, line_a.a[0], a_c))

    if a_m == b_m:
        # They are parallel
        print("They are parellel")
        return False

    # a_m*x + a_c = b_m*x + b_c
    x_intercept = (b_c - a_c) / (a_m - b_m)
    y_intercept = a_m*x_intercept + a_c

    # Check if the intercepts are within the line_b segment
    max_x = max(line_b.a[0], line_b.b[0])
    min_x = min(line_b.a[0], line_b.b[0])
    max_y = max(line_b.a[1], line_b.b[1])
    min_y = min(line_b.a[1], line_b.b[1])

    if not ((x_intercept > min_x) and (x_intercept < max_x) and (y_intercept > min_y) and (y_intercept < max_y)):
        # Intercept doesn't lie on the segment
        print("Intercept is out of range")
        return False

    return (x_intercept, y_intercept)

def get_magnitude(line: Line):
    dy = abs(line.a[1] - line.b[1])
    dx = abs(line.a[0] - line.a[0])
    return maths.sqrt(dy^2 + dx^2)

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
                    print("Merging lines {} and {}".format(surrounding_line, line))
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
