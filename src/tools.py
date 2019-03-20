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

    def __eq__(self, other):
        return (self.a == other.a) and (self.b == other.b)

    def inverse(self):
        return self.__class__(self.b, self.a)

class LineSet:
    def __init__(self, remove_duplicates=False):
        self.remove_duplicates = remove_duplicates
        self.__contain_context = None
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
        def lamb(l):
            if (l.a == line.a and l.b == line.b):
                self.__contain_context = 'NORMAL'
                return True
            elif (l.a == line.b and l.b == line.a):
                self.__contain_context = 'INVERT'
                return True

        exists = len(
            list(
                filter(
                    lamb,
                    self.lines
                )
            )
        )

        if not exists:
            self.__contain_context = None

        return True if exists else False

    def add(self, line: Line) -> None:
        if self.remove_duplicates:
            if line in self:
                if self.__contain_context == 'INVERT':
                    self.duplicates.append(line.invert())
                elif self.__contain_context == 'NORMAL':
                    self.duplicates.append(line)
            else:
                self.lines.append(line)

        else:
            print("Adding line {}".format(line))
            if line in self:
                print("Line in self {}".format(self.__contain_context))
                if self.__contain_context == 'INVERT':
                    self.duplicates.append(line.invert())
                elif self.__contain_context == 'NORMAL':
                    self.duplicates.append(line)

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

    ls = LineSet(remove_duplicates=True)
    ls.add(line)
    print("LS contains line {}".format(line in ls))
    print("LS contains other {}".format(other in ls))
    print("LS contains yo {}".format(yo in ls))
