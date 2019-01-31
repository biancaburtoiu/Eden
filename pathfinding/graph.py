import queue as Q
from math import sqrt


class Graph:

    def __init__(self):
        self.root = Node((0, 0))

    def searchGraph(self, start, goal):
        # initially we have a priority queue of nodes, ordered by distance
        # (assuming all distances are 1), and an empty result set
        open_set = Q.PriorityQueue()
        open_set.put((start, 0))
        closed = []

        while not open_set.empty():
            current = open_set.get()
            if current.pos == goal.pos:
                None
                # work out path
            else:
                closed.append(current)
                for neighbour in current.getNeighbours():
                    cost = neighbour.getCost() + 1  # (node distances are 1)
                    if neighbour not in closed or cost < neighbour.getCost():
                        neighbour.setCost(cost)
                        open_set.put((neighbour,cost+sld(neighbour,goal)))


class Node:
    def __init__(self, pos):
        self.pos = pos

        # (node,direction) pairs!
        # direction should be l,r,u,d
        self.neighbours = []

        self.cost=0

    def getPos(self):
        return self.pos

    def getNeighbours(self):
        return self.neighbours

    # neighbour argument should be a pair: (Node obj, direction)
    def addNeighbour(self, n):
        self.neighbours.append(n)

    def getCost(self):
        return self.cost

    def setCost(self,c):
        self.cost = c

# calculate euclidean distance between two nodes
def sld(node1,node2):
    return sqrt(node1.getPos()^2 + node2.getPos()^2)
