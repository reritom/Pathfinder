from functools import reduce
from typing import List

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
    def __init__(self, a: tuple, b: tuple):
        self.a = a
        self.b = b

    def __repr__(self):
        return str((self.a, self.b))

class LineSet:
    def __init__(self):
        self.lines = []

    def __contains__(self, line: Line) -> bool:
        exists = len(
            list(
                filter(
                    lambda l:
                    (l.a == line.a and l.b == line.b) or (l.a == line.b and l.b == line.a),
                    self.lines
                )
            )
        )

        return exists

    def add(self, line: Line) -> None:
        if line not in self:
            self.lines.append(line)

    def extend(self, lines: List[Line]) -> None:
        for line in lines:
            self.add(line)

    def __len__(self) -> int:
        return len(self.lines)

if __name__=='__main__':
    line = Line((0, 0), (5, 10))
    other = Line((5, 10), (0, 0))
    yo = Line((0, 10), (0, 0))

    ls = LineSet()
    ls.add(line)
    print("LS contains line {}".format(line in ls))
    print("LS contains other {}".format(other in ls))
    print("LS contains yo {}".format(yo in ls))
