import queue as Q
from math import sqrt

# ================= Graph class: references root node, and provides operations==
class Graph:

    def __init__(self,pos=(0,0)):
        self.root = Node(pos)

    def searchGraph(self, goal_pos):
        # initially we have a priority queue of nodes:
        #   queue is ordered by cost so far + heuristic estimate to goal
        # we also have a map from Node to cost so far
        # and a map from node to node's parent, so we can work out the
        # best route from the start to a specific node

        start = self.root # start from root of graph
        open_set = Q.PriorityQueue()
        open_set.put((0,start))
        cost_so_far={}
        parent = {}
        cost_so_far[start] = 0

        while not open_set.empty():
            # take the lowest cost node first
            (_,current) = open_set.get()
            if current.getPos() == goal_pos:
                # in this case, this is our goal
                return self.constructPath(parent, current,start)
                # work out path

            else:
                # we must keep exploring

                for neighbour,_ in current.getNeighbours():
                    cost = cost_so_far[current] + 1  # (node distances are 1)
                    if neighbour not in cost_so_far.keys() or cost < cost_so_far[neighbour]:
                        # we have found the best route to this node (so far)
                        cost_so_far[neighbour] = cost
                        # note use of sld() as a measure of goal closeness
                        cost_for_node = int(cost+mbd(neighbour,Node(goal_pos)))
                        open_set.put( ( cost_for_node, neighbour ) )
                        parent[neighbour] = current

    def constructPath(self,parent_dict, goal,start):
        # start at the goal
        current = goal
        # this will be a list of nodes, in order
        node_path=[current]

        # until we get to the start..
        while current != start:
            # follow the parents back to the start
            current = parent_dict[current]
            # tracking which nodes we pass through
            node_path.insert(0, current)


        dir_path = []
        #now convert the path into a list of directions
        for i in range(0,len(node_path)-1):
            dir_path.append(node_path[i].dirToNeighbour(node_path[i+1]))

        return node_path,dir_path

    # takes a starting position pair, and a 2d bool grid of visitable squares
    # and turns it into a graph structure
    def pathFromGrid(self,start_pos,grid):
        # sychronise root note and starting position
        self.root.setPos(start_pos)

        # we will have a stack of nodes to visit
        node_stack = [self.root]

        # list of co ords, relative to us, that we want to visit
        COORD_DIFFS = [((0,1),'u'),((-1,0),'l'),((0,-1),'d'),((1,0),'r')]
        while (len(node_stack)):
            current = node_stack.pop()
            (x,y) = current.getPos()

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

                    procedural way'''

            # list comprehension of above. Adds the absolute co ords to list
            # only if they are within the boundary of the grid
            neighbour_coords = [((a+x,b+y),d) for ((a,b),d) in COORD_DIFFS
                if x+a in range(0,len(grid[0])) and y+b in range(0,len(grid))]

            #now loop through remaining coords - these are the neighbours in the grid
            for ((x,y),d) in neighbour_coords:
                if grid[y][x]==0:
                    # an unvisited, clear square. make a node and add it to stack
                    grid[y][x] = Node((x,y))
                    node_stack.append(grid[y][x])

                    # note the ==0 case still falls through vv
                if grid[y][x]!=1:
                    # any square that isn't an obstacle

                    grid[y][x].addNeighbour((invert(d),current))
                    current.addNeighbour((d,grid[y][x]))

# ============== Node class: should not be used individually, used by Graph to=
# ==============represent a node===============================================
class Node:
    def __init__(self, pos):
        # tuple co ordinate
        self.pos = pos

        # dictionary mapping directions ('l','r','u','d') to nodes!
        self.neighbours = {}


    def __lt__(self,other):
        return 1

    def __repr__(self):
        return "(" + str(self.pos[0])+","+str(self.pos[1])+ ")"

    def __str__(self):
        return "(" + str(self.pos[0])+","+str(self.pos[1])+ ")"

    def getPos(self):
        return self.pos

    def setPos(self, new_pos):
        self.pos=new_pos

    def getNeighbours(self):
        return self.neighbours.items()

    # neighbour argument should be a pair: (Node obj, direction)
    def addNeighbour(self, n):
        self.neighbours[n[1]]=n[0]

    # returns direction from this node to neighbour node

    #####rename it
    def dirToNeighbour(self,neighbour):
        return self.neighbours[neighbour]


# calculate euclidean distance between two nodes
def sld(node1,node2):
    (x1,y1) = node1.getPos()
    (x2,y2) = node2.getPos()
    return sqrt((x1-x2)**2 + (y1-y2)**2)

# calculate manhatton block distance between two nodes
def mbd(node1,node2):
    (x1,y1) = node1.getPos()
    (x2,y2) = node2.getPos()
    return abs(x1-x2) + abs(y1-y2)

def invert(d):
    if d=='d':
         return 'u'
    if d=='u':
         return 'd'
    if d=='l':
         return 'r'
    else:
         return 'l'

def gridprint(grid):
    grid.reverse()
    for row in grid:
        print(row)

def main():
    grid = [[0,1,0],[0,0,0],[0,0,0]]
    gridprint(grid.copy())
    target = (2,0)
    print("target: ",target)
    graph = Graph()
    graph.pathFromGrid((0,0),grid)
    print(graph.searchGraph(target))

if __name__ == "__main__":
    main()
