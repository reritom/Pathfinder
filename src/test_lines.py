from .tools import Line, merge_lines, get_intersection, line_from_radial
import unittest
import math as maths

class TestMergeLines(unittest.TestCase):
    def test_merge_lines(self):
        # Create a rectangle shape as such with segments of 1 unit length
        lines_to_merge = [
            Line((0, 0), (0, 1)),
            Line((0, 1), (1, 1)),
            Line((1, 1), (2, 1)),
            Line((2, 1), (2, 0)),
            Line((2, 0), (1, 0)),
            Line((1, 0), (0, 0))
        ]

        # When we merge, we expect the two longer sides to merge from 2 lines each, to 1 line each
        merged = merge_lines(lines_to_merge)

        self.assertEqual(len(merged), 4)
        self.assertTrue(Line((0, 0), (0, 1)) in merged)
        self.assertTrue(Line((0, 1), (2, 1)) in merged)
        self.assertTrue(Line((2, 1), (2, 0)) in merged)
        self.assertTrue(Line((2, 0), (0, 0)) in merged)

        print("Test merge lines OK")

    def test_get_intersection(self):
        line_a = Line(
            (0, 0),
            (10, 10)
        )

        line_b = Line(
            (0, 10),
            (10, 0)
        )

        intersection = get_intersection(line_a, line_b)
        self.assertEqual(intersection, (5, 5))

    def test_get_intersection_parallel(self):
        line_a = Line(
            (0, 0),
            (10, 10)
        )

        line_b = Line(
            (1, 0),
            (11, 10)
        )

        intersection = get_intersection(line_a, line_b)
        self.assertEqual(intersection, False)

    def test_get_intersection_out_of_range(self):
        line_a = Line(
            (0, 0),
            (10, 10)
        )

        line_b = Line(
            (0, 10),
            (2, 8)
        )

        intersection = get_intersection(line_a, line_b)
        self.assertEqual(intersection, False)

    def test_line_from_radial(self):
        line = line_from_radial((0, 0), 0.785398, maths.sqrt(200))

        self.assertEqual(line.a, (0, 0))
        self.assertEqual((round(line.b[0]), round(line.b[1])), (10, 10))
