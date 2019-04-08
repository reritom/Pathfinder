from .tools import (
    Line,
    merge_lines,
    get_intersection,
    line_from_radial,
    lies_between,
    get_magnitude,
    is_adjacent,
    is_corner_adjacent,
    get_artificial_blocks
)
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
        self.assertEqual(intersection, "PARALLEL")

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

    def test_is_adjacent_true(self):
        self.assertTrue(is_adjacent((0, 0), (1, 1)))
        self.assertTrue(is_adjacent((0, 0), (1, 0)))
        self.assertTrue(is_adjacent((0, 0), (0, 1)))

    def test_is_adjacent_false(self):
        self.assertFalse(is_adjacent((0, 0), (2, 2)))

    def test_is_corner_adjacent_true(self):
        self.assertTrue(is_corner_adjacent((0, 0), (1, 1)))
        self.assertTrue(is_corner_adjacent((0, 0), (-1, -1)))

    def test_is_corner_adjacent_false(self):
        self.assertFalse(is_corner_adjacent((0, 0), (1, 0)))

    def test_get_magnitude(self):
        line = Line((0, 0), (5, 5))
        self.assertEqual(int(get_magnitude(line)), int(maths.sqrt(5**2 + 5**2)))

    def test_line_from_radial(self):
        line = line_from_radial((0, 0), 0.785398, maths.sqrt(200))

        self.assertEqual(line.a, (0, 0))
        self.assertEqual((round(line.b[0]), round(line.b[1])), (10, 10))

    def test_lies_between_correct(self):
        self.assertTrue(lies_between((1, 1), (0, 0), (3, 3)))
        self.assertTrue(lies_between((1, 2), (1, 1), (1, 3)))
        self.assertTrue(lies_between((1, 2), (1, 1), (2, 3)))
        self.assertTrue(lies_between((1, 2), (1, 1), (2, 3)))
        self.assertTrue(lies_between((3, 0), (1, 0), (4, 0)))
        self.assertTrue(lies_between((3, 0), (1, 1), (4, 0)))
        print("RFHEY")
        self.assertTrue(lies_between((4, 0), (0, 1), (5, 0)))
        print("END")
    """
    def test_lies_between_false(self):
        self.assertFalse(lies_between((10, 10), (0, 0), (3, 3)))
        self.assertFalse(lies_between((1, 1), (0, 0), (2, 0)))
        self.assertFalse(lies_between((2, 1), (0, 0), (2, 0)))

    def test_get_artificial_blocks(self):
        artificial_blocks = get_artificial_blocks(
            (0, 0),
            [(1, 0), (0, 1)]
        )

        expected_artificial_block = (1, 1)
        self.assertIn(expected_artificial_block, artificial_blocks)
    """
