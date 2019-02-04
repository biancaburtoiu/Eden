import unittest
from graph import *

class GraphTestingMethods(unittest.TestCase):

    def test_dontMove(self):
        grid = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        target = (0,0)
        result, _, _ = getPathLengthFromGrid(grid,target)
        self.assertEqual(result, 1)

    def test_moveOnce(self):
        grid = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        target = (1, 0)
        result, _, _ = getPathLengthFromGrid(grid, target)
        self.assertEqual(result, 2)

    def test_shortPath(self):
        grid = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        target = (2,1)
        result, _, _ = getPathLengthFromGrid(grid,target)
        self.assertEqual(result, 4)

    def test_smallObstacle(self):
        grid = [
            [0, 1, 0],
            [0, 1, 0],
            [0, 0, 0],
        ]
        target = (2,1)
        result, path, _ = getPathLengthFromGrid(grid,target)
        self.assertEqual(result, 6)

    def test_noPath(self):
        grid = [
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0],
        ]
        target = (2,0)
        result, path, _ = getPathLengthFromGrid(grid,target)
        self.assertEqual(result, 0)

    def test_spiral(self):
        grid = [
            [0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0],

        ]
        target = (4, 3)
        result, path, _ = getPathLengthFromGrid(grid, target)
        self.assertEqual(result, 24)

    def test_multiPath(self):
        grid = [
            [1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0],
            [1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [1, 0, 0, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],

        ]
        target = (4, 2)
        result, path, _ = getPathLengthFromGrid(grid, target,(2,2))
        self.assertEqual(result, 9)

    def test_multiPathEqLen(self):
        grid = [
            [1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0],
            [1, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [1, 0, 0, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],

        ]
        target = (4, 3)
        result, path, _ = getPathLengthFromGrid(grid, target,(2,2))
        self.assertEqual(result, 10)

if __name__ == '__main__':
    unittest.main()