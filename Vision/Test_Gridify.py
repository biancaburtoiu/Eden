import unittest
import numpy as np
from Vision import Gridify


def array_to_string(arr):
    result = "["
    for r in range(0, len(arr)):
        result += "\n    %s" % arr[r]
    result += "\n]"
    return result


class TestConvertThreshToMap(unittest.TestCase):

    def setUp(self):
        self.img = np.zeros((5, 5, 3), dtype=np.uint8)

    def test_top_left(self):
        self.img[0, 0] = np.ones((3), dtype=np.uint8) * 255
        expected = [
            [1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        result = Gridify.convert_thresh_to_map(self.img, cell_length=2, shift_amount=1)
        self.assertEqual(len(expected), len(result), "Heights of expected and result differ")
        self.assertEqual(len(expected[0]), len(result[0]), "Widths of expected and result differ")
        for i in range(0, len(expected)):
            for j in range(0, len(expected[0])):
                self.assertEqual(expected[i][j], result[i][j],
                                 "Expected and results differ in elements.\nExpected:\n%s\nResult:\n%s\n" % (
                                     expected, result))

    def test_top_right(self):
        self.img[0, 4] = np.ones((3), dtype=np.uint8) * 255
        expected = [
            [0, 0, 0, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        result = Gridify.convert_thresh_to_map(self.img, cell_length=2, shift_amount=1)
        self.assertEqual(len(expected), len(result), "Heights of expected and result differ")
        self.assertEqual(len(expected[0]), len(result[0]), "Widths of expected and result differ")
        for i in range(0, len(expected)):
            for j in range(0, len(expected[0])):
                self.assertEqual(expected[i][j], result[i][j],
                                 "Expected and results differ in elements.\nExpected:\n%s\nResult:\n%s\n" % (
                                     expected, result))

    def test_bottom_left(self):
        self.img[4, 0] = np.ones((3), dtype=np.uint8) * 255
        expected = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 0, 0, 0]
        ]
        result = Gridify.convert_thresh_to_map(self.img, cell_length=2, shift_amount=1)
        self.assertEqual(len(expected), len(result), "Heights of expected and result differ")
        self.assertEqual(len(expected[0]), len(result[0]), "Widths of expected and result differ")
        for i in range(0, len(expected)):
            for j in range(0, len(expected[0])):
                self.assertEqual(expected[i][j], result[i][j],
                                 "Expected and results differ in elements.\nExpected:\n%s\nResult:\n%s\n" % (
                                     expected, result))

    def test_bottom_right(self):
        self.img[4, 4] = np.ones((3), dtype=np.uint8) * 255
        expected = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1]
        ]
        result = Gridify.convert_thresh_to_map(self.img, cell_length=2, shift_amount=1)
        self.assertEqual(len(expected), len(result), "Heights of expected and result differ")
        self.assertEqual(len(expected[0]), len(result[0]), "Widths of expected and result differ")
        for i in range(0, len(expected)):
            for j in range(0, len(expected[0])):
                self.assertEqual(expected[i][j], result[i][j],
                                 "Expected and results differ in elements.\nExpected:\n%s\nResult:\n%s\n" % (
                                     expected, result))

    def test_almost_full(self):
        for i in range(1, 4):
            for j in range(1, 4):
                self.img[i, j] = np.ones((3), dtype=np.uint8) * 255
        expected = [
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1]
        ]
        result = Gridify.convert_thresh_to_map(self.img, cell_length=2, shift_amount=1)
        self.assertEqual(len(expected), len(result), "Heights of expected and result differ")
        self.assertEqual(len(expected[0]), len(result[0]), "Widths of expected and result differ")
        for i in range(0, len(expected)):
            for j in range(0, len(expected[0])):
                self.assertEqual(expected[i][j], result[i][j],
                                 "Expected and results differ in elements.\nExpected:\n%s\nResult:\n%s\n" % (
                                     expected, result))

    def test_full(self):
        for i in range(0, 5):
            for j in range(0, 5):
                self.img[i, j] = np.ones((3), dtype=np.uint8) * 255
        expected = [
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1]
        ]
        result = Gridify.convert_thresh_to_map(self.img, cell_length=2, shift_amount=1)
        self.assertEqual(len(expected), len(result), "Heights of expected and result differ")
        self.assertEqual(len(expected[0]), len(result[0]), "Widths of expected and result differ")
        for i in range(0, len(expected)):
            for j in range(0, len(expected[0])):
                self.assertEqual(expected[i][j], result[i][j],
                                 "Expected and results differ in elements.\nExpected:\n%s\nResult:\n%s\n" % (
                                     expected, result))

    def test_full_rhs(self):
        for i in range(0, 5):
            for j in range(0, 2):
                self.img[i, j] = np.ones((3), dtype=np.uint8) * 255
        expected = [
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 1, 0, 0]
        ]
        result = Gridify.convert_thresh_to_map(self.img, cell_length=2, shift_amount=1)
        self.assertEqual(len(expected), len(result), "Heights of expected and result differ")
        self.assertEqual(len(expected[0]), len(result[0]), "Widths of expected and result differ")
        for i in range(0, len(expected)):
            for j in range(0, len(expected[0])):
                self.assertEqual(expected[i][j], result[i][j],
                                 "Expected and results differ in elements.\nExpected:\n%s\nResult:\n%s\n" % (
                                     expected, result))

    def test_larger_shift(self):
        for i in range(0, 5):
            for j in range(0, 2):
                self.img[i, j] = np.ones((3), dtype=np.uint8) * 255
        expected = [
            [1, 0],
            [1, 0]
        ]
        result = Gridify.convert_thresh_to_map(self.img, cell_length=2, shift_amount=2)
        self.assertEqual(len(expected), len(result), "Heights of expected and result differ")
        self.assertEqual(len(expected[0]), len(result[0]), "Widths of expected and result differ")
        for i in range(0, len(expected)):
            for j in range(0, len(expected[0])):
                self.assertEqual(expected[i][j], result[i][j],
                                 "Expected and results differ in elements.\nExpected:\n%s\nResult:\n%s\n" % (
                                     expected, result))

