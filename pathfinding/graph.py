import queue as Q

class Graph:

    def __init__(self):
        self.root = Node((0,0))

    def pathNotFound(self,openSet,goal):
        lowestCostNode = openSet.get()
        openSet.put(lowestCostNode)
        return lowestCostNode.pos == goal.pos

    def searchGraph(self,node1,node2):
        #initially we have a priority queue of nodes, ordered by distance
        #(assuming all distances are 1), and an empty result set
        openSet = Q.PriorityQueue()
        openSet.put(node1)
        closed = []

        while self.pathNotFound(openSet,node2):
            current = openSet.get(self)






class Node:
    def __init__(self,pos):
        # a list of neighbour nodes 
        self.pos=pos
        self.up=None
        self.down=None
        self.left=None
        self.right=None

    def addUpNeighbour(self,n):
        self.up=n

    def addDownNeighbour(self,n):
        self.down=n

    def addLeftNeighbour(self,n):
        self.left=n

    def addRightNeighbour(self,n):
        self.right=n

    def getPos(self):
        return self.pos


