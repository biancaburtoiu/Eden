import unittest
from graph import *

class GraphTestingMethods(unittest.TestCase):

    def test_smallObstacle(self):
        grid = [
            [0, 1, 0],
            [0, 1, 0],
            [0, 0, 0],
        ]
        target = (2,1)
        result, _ , _,insts = getInstructionsFromGrid(grid,target)
        self.assertEqual(insts, ['u', ('m', 2), ('r', 90), ('m', 2), ('r', 90), ('m', 1)])

    def test_noPath(self):
        grid = [
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0],
        ]
        target = (2,0)
        result, path, _, insts = getInstructionsFromGrid(grid,target)
        self.assertEqual(insts,[])

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
        result, path, _, insts = getInstructionsFromGrid(grid, target)
        self.assertEqual(insts,['u', ('m', 5), ('r', 90), ('m', 6), ('r', 90), ('m', 4), ('r', 90), 
            ('m', 4), ('r', 90), ('m', 2), ('r', 90), ('m', 2)] )

    def test_windypath(self):
        grid = [[0, 0, 0, 1, 0, 0, 0],
                [0, 1, 0, 0, 0, 1, 0],
                [0, 0, 1, 1, 1, 0, 0],
                [1, 0, 1, 0, 1, 0, 1],
                [0, 0, 1, 0, 1, 0, 0],
                [0, 1, 1, 0, 1, 1, 0],
                [0, 0, 1, 0, 0, 0, 0]]
        target = (1,0)
        start = (3,3)
        _,_,_,insts = getInstructionsFromGrid(grid, target, start)
        self.assertEqual(insts, ['u', ('m', 3), ('r', 90), ('m', 3), ('r', 90), ('m', 2), ('r', 90), ('m', 1),
         ('r', -90), ('m', 2), ('r', -90), ('m', 1), ('r', 90), ('m', 2), ('r', 90), ('m', 2), ('r', 90), 
         ('m', 1), ('r', -90),('m', 2), ('r', -90), ('m', 1), ('r', 90), ('m', 1)])

    def test_zig_zag(self):
        grid = [
            [0, 1, 1, 1, 0, 1, ],
            [0, 0, 1, 0, 0, 0, ],
            [1, 0, 1, 0, 1, 0, ],
            [1, 0, 0, 0, 1, 0, ],
            [0, 1, 1, 1, 0, 0, ],
            [0, 0, 0, 0, 0, 1, ],
        ]
        target = (0,5)
        _,_,_,insts = getInstructionsFromGrid(grid, target)
        self.assertEqual(insts, ['u', ('m', 1), ('r', 90), ('m', 1),
          ('r', -90), ('m', 2), ('r', 90), ('m', 2), ('r', 90), ('m', 2),
           ('r', -90), ('m', 2), ('r', -90), ('m', 3), ('r', -90), ('m', 1),
            ('r', 90), ('m', 1), ('r', -90), ('m', 4)],)

    def test_snake(self):
        grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        ]

        target = (12,13)
        _,_,_,insts = getInstructionsFromGrid(grid, target)
        self.assertEqual(insts, ['r', ('m', 12), ('r', -90), ('m', 2), ('r', -90), ('m', 12),
         ('r', 90), ('m', 2), ('r', 90), ('m', 12), ('r', -90), ('m', 2), ('r', -90), ('m', 12),
          ('r', 90), ('m', 2), ('r', 90), ('m', 12), ('r', -90), ('m', 2), ('r', -90), ('m', 12),
           ('r', 90), ('m', 2), ('r', 90), ('m', 12),('r',-90),('m',1)])



if __name__ == '__main__':
    unittest.main()