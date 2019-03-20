import unittest
from .tools import Line, LineSet


class TestLine(unittest.TestCase):
    def test_line(self):
        line = Line(
            (0, 0),
            (10, 10)
        )

        self.assertEqual(line.a, (0, 0))
        self.assertEqual(line.b, (10, 10))

    def test_line_set_add(self):
        line = Line(
            (0, 0),
            (10, 10)
        )

        opposite_line = Line(
            (10, 10),
            (0, 0)
        )

        line_set = LineSet()
        line_set.add(line)

        self.assertTrue(line in line_set)
        self.assertEqual(len(line_set), 1)

        # Even though the opposite line hasn't been added, the line set does contain the directionless line
        self.assertTrue(opposite_line in line_set)

        line_set.add(opposite_line)

        # The opposite line shouldn't be added
        self.assertEqual(len(line_set), 1)

    def test_line_set_extend(self):
        line_set = LineSet()
        x, y = 0, 0

        lines = [
            Line((x, y), (x, y+1)),
            Line((x, y), (x+1, y+1)),
            Line((x+1, y), (x+1, y+1)),
            Line((x, y+1), (x+1, y+1)),
            Line((x, y), (x, y+1)), # From here, these are duplicates
            Line((x, y), (x+1, y+1)),
            Line((x+1, y), (x+1, y+1)),
            Line((x, y+1), (x+1, y+1))
        ]

        line_set.extend(lines)

        self.assertEqual(len(line_set), 4)
