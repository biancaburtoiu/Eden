import queue as Q
from math import sqrt
from sys import argv


# ================= Graph class: references root node, and provides operations==
class Graph:

    def __init__(self, pos=(0, 0)):
        self.root = Node(pos)

    # perform A* on this graph, starting at the start Node, and finding a path to
    # the (x,y) pair given as goal_pos.
    # it will return an ordered list of directions ('u','d','l','r')
    def searchGraph(self, goal_pos):
        # initially we have a priority queue of nodes:
        #   queue is ordered by cost so far + heuristic estimate to goal
        # we also have a map from Node to cost so far
        # and a map from node to node's parent, so we can work out the
        # best route from the start to a specific node

        start = self.root  # start from root of graph
        open_set = Q.PriorityQueue()  # description of this structure near of Node class
        open_set.put((0, start))
        cost_so_far = {}
        parent = {}
        cost_so_far[start] = 0

        # continue until we've found all the nodes, unless the goal is reached
        while not open_set.empty():
            # take the lowest cost node first
            (_, current) = open_set.get()

            if current.getPos() == goal_pos:
                # in this case, this is our goal
                return self.constructPath(parent, current, start)

            else:
                # we must keep exploring

                for (neighbour, _) in current.getNeighbours():
                    cost = cost_so_far[current] + 1  # (node distances are 1)
                    if neighbour not in cost_so_far.keys() or cost < cost_so_far[neighbour]:
                        # we have found the best route to this node (so far)
                        cost_so_far[neighbour] = cost
                        # note use of sld()/mbd() as a measure of goal closeness
                        cost_for_node = int(cost + mbd(neighbour, Node(goal_pos)))
                        open_set.put((cost_for_node, neighbour))
                        parent[neighbour] = current

        # we didn't find the goal! return None twice because the other return branch will also return two items.
        # avoids NoneType not iterable error
        return None, None

    def constructPath(self, parent_dict, goal, start):
        # start at the goal
        current = goal
        # this will be a list of nodes, in order
        node_path = [current]

        # until we get to the start..
        while current != start:
            # follow the parents back to the start
            current = parent_dict[current]
            # tracking which nodes we pass through
            node_path.insert(0, current)

        dir_path = []
        # now convert the path into a list of directions
        for i in range(0, len(node_path) - 1):
            dir_path.append(node_path[i].neighbourToDir(node_path[i + 1]))

        return node_path, dir_path

    # takes a starting position pair, and a 2d bool grid of visitable squares
    # and turns it into a graph structure
    # A grid square is 0 iff the square is accessible
    def graphFromGrid(self, start_pos, grid):
        # sychronise root note and starting position
        self.root.setPos(start_pos)

        # we will have a stack of nodes to visit
        node_stack = [self.root]

        # list of co ords, relative to us, that we want to visit. They are stored as
        # ( (x-pos, y-pos) , direction) nested pairs
        COORD_DIFFS = [((0, 1), 'u'), ((-1, 0), 'l'), ((0, -1), 'd'), ((1, 0), 'r')]

        # continue until we've visited every node
        while len(node_stack):
            current = node_stack.pop()
            (x, y) = current.getPos()

            # make the absolute co ords for the given current node

            '''procedural way

            coords=[]
            for coord,d in COORD_DIFFS:
                # order is significant here
                x_p = coord[0]+x
                y_p = coord[1] + y
                if x_p>=0 and y_p>= 0 and x_p < len(grid[0]) and y_p < len(grid):

                    #print("("+str(x_p)+","+str(y_p) + ") - " + d)

                    new_element = ((x_p,y_p),d)

                    #print(new_element)

                    coords.append(new_element)

                    end procedural way'''

            # list comprehension of above. Adds the absolute co ords to list
            # only if they are within the boundary of the grid
            neighbour_coords = [((a + x, b + y), d) for ((a, b), d) in COORD_DIFFS
                                if x + a in range(0, len(grid[0])) and y + b in range(0, len(grid))]

            # now loop through remaining coords - these are the neighbours in the grid
            for ((x, y), d) in neighbour_coords:
                if grid[y][x] == 0:
                    # an unvisited, clear square. make a node and add it to stack
                    grid[y][x] = Node((x, y))
                    node_stack.append(grid[y][x])

                    # note the ==0 case still falls through vv
                if grid[y][x] != 1:
                    # any square that isn't an obstacle

                    # create mutual neighbouring relation
                    grid[y][x].addNeighbour((invert(d), current))
                    current.addNeighbour((d, grid[y][x]))

                # anything that misses both ifs is an obstacle, ignore it!

        # the grid is now in graph form. This Graph object references the node for start_pos

    # for debugging, turns our graph into a grid.
    # pass in the size of the grid, if it's too small this will probably crash
    def gridFromGraph(self, size):
        # create grid using list comprehension, assumes everything is obstacle initially
        grid = [[1] * size[0] for i in range(0, size[1])]

        node_stack = [self.root]
        visited = []
        while len(node_stack):
            current = node_stack.pop()
            visited.append(current)

            (x, y) = current.getPos()
            try:
                grid[y][x] = 0
            except:
                None

            for (n, _) in current.getNeighbours():
                if n not in visited:
                    node_stack.append(n)

        return grid


# ============== Node class: should not be instantiated individually, used by Graph to=
# ==============represent a node and it's neighbours===================================
class Node:
    def __init__(self, pos):
        # tuple co ordinate
        self.pos = pos

        # dictionary mapping nodes to directions
        self.neighbours = {}

    # the priority queue contains tuples of (score,Node). If scores are equal, it tries to compare nodes.
    # if the score is the same, we don't care. So we implement a trivial comparison function for python to use
    def __lt__(self, other):
        return 1

    def __repr__(self):
        return "(" + str(self.pos[0]) + "," + str(self.pos[1]) + ")"

    def __str__(self):
        return "(" + str(self.pos[0]) + "," + str(self.pos[1]) + ")"

    def getPos(self):
        return self.pos

    def setPos(self, new_pos):
        self.pos = new_pos

    def getNeighbours(self):
        return self.neighbours.items()

    # neighbour argument should be a pair: (directiom, Node Obj)
    def addNeighbour(self, n):
        self.neighbours[n[1]] = n[0]

    # returns direction from this node to neighbour node
    def neighbourToDir(self, neighbour):
        return self.neighbours[neighbour]


# ==============Main program==================================================

# =====heuristics====

# calculate euclidean distance between two nodes
def sld(node1, node2):
    (x1, y1) = node1.getPos()
    (x2, y2) = node2.getPos()
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# calculate manhatton block distance between two nodes
def mbd(node1, node2):
    (x1, y1) = node1.getPos()
    (x2, y2) = node2.getPos()
    return abs(x1 - x2) + abs(y1 - y2)


# ====helpers======

# up is opposite of down, etc
def invert(d):
    if d == 'd':
        return 'u'
    if d == 'u':
        return 'd'
    if d == 'l':
        return 'r'
    else:
        return 'l'


# prints a grid
def gridprint(grid):
    gridcopy = grid.copy()
    gridcopy.reverse()
    for row in gridcopy:
        print(row)


# plots path on a grid
def plotPath(grid, path):
    if path is not None:
        for node in path:
            (x, y) = node.getPos()
            grid[y][x] = 5
    return grid


# given a grid, calculates shortest path and returns it's length
def getPathLengthFromGrid(grid, target, start=(0, 0)):
    graph = Graph()
    graph.graphFromGrid(start, grid)
    path, dirs = graph.searchGraph(target)
    length = 0
    if path is not None:
        length = len(path)

    return length, path, dirs


# =====main=======

def main():
    print(len(argv))
    if len(argv) > 0 and argv[1] == 'f':
        # read grid from grid.txt

        '''
        usage: call as 'python3 f [a,b] [x,y]'
        f   - denotes read from file. The file 'grid.txt' will be read.
            - put your grid in here, with  (0,0) at the bottom, taking a new line for each row,
             and comma separating within a row  -- '0,0,1,0'
        [a,b]   - the starting position (a,b)
        [x,y]   - the target position (x,y)
        '''

        grid_file = open("grid.txt", "r")
        start = (int(argv[2][1]), int(argv[2][3]))
        target = (int(argv[3][1]), int(argv[3][3]))

        grid = []
        for line in grid_file:
            line_as_char_list = line.strip().split(',')
            line_as_list = [int(x) for x in line_as_char_list]
            grid.insert(0, line_as_list)  # we must turn the grid 'upside down' for python

    else:
        # hard coded grid

        # watch out because this grid is upside down ((0,0) top left
        # but the co ordinate system works normally ((0,0) bottom left
        # - the gridprint function will flip the grid for you

        grid = [
            [0, 0, 0, 0, 1, 0, 0, 1],
            [0, 1, 0, 0, 1, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
        ]
        target = (6, 0)
        start = (0, 0)

    gridprint(grid)

    print("target: ", target)
    graph = Graph()
    graph.graphFromGrid(start, grid)
    path, dirs = graph.searchGraph(target)
    gridprint(plotPath(graph.gridFromGraph((len(grid[0]), len(grid))), path))
    print(dirs)
    if path is not None:
        print("length: ", len(path))
    else:
        print("no path!")


if __name__ == "__main__":
    main()
