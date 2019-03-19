def surroundings_of(point):
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

class Line:
    def __init__(self, point_a, point_b):
        self.point_a = point_a
        self.point_b = point_b

class LineSet:
    def __init__(self):
        self.lines = []

    def add(self, line):
        pass
