"""
Calculate best path and path benefits.
Includes vertices and edges.
"""

import re
import igraph
import colorsys
from appJar import gui
from sortedcollections import ValueSortedDict


class Board:
    """
    Store square weight and calculate optimal paths between them.
    """


    def __init__(self, size):
        """
        Initialize the Graph class.

        param1: integer - size of board
        """

        self.checkInt(size) # comment this out for speed

        if size <= 1:
            raise ValueError('size must be greater than 1')

        self.size = size  # declare size instance variable

        self.graph = igraph.Graph(directed=True)  # declare graph
        for row in range(size + 1):  # create vertices
            for col in range(size + 1):
                self.graph.add_vertex(name=str(row) + ',' + str(col))

        for row in range(size):  # create 1/2 edges
            for col in range(size):
                self.graph.add_edge(str(row) + ',' + str(col),
                                    str(row) + ',' + str(col + 1), weight=50.0)
                self.graph.add_edge(str(row) + ',' + str(col), str(row + 1) +
                                    ',' + str(col), weight=50.0)

        for row in range(1, size + 1):  # create other 1/2 edges
            for col in range(1, size + 1):
                self.graph.add_edge(str(row) + ',' + str(col), str(row) + ',' +
                                    str(col - 1), weight=50.0)
                self.graph.add_edge(str(row) + ',' + str(col), str(row - 1) +
                                    ',' + str(col), weight=50.0)

        self.dictionary = ValueSortedDict()
        for row in range(0, size):  # populate dictionary
            for col in range(0, size):
                self.dictionary[str(row) + ',' + str(col)] = 50.0

        self.edges = dict()
        for row in range(0, size):  # save edges incident to each vertex
            for col in range(0, size):
                vertexId = self.graph.vs.find(str(row) + ',' + str(col))
                edges = self.graph.incident(vertexId) # list of edges
                edges = [self.graph.es.find(edge) for edge in edges]
                self.edges[str(row) + ',' + str(col)] = edges


    def checkNode(self, u):
        """
        Check if u is a valid node.

        param1: string - node in the form <integer>,<integer>
        """

        match = re.match('^(\\d+),(\\d+)$', u)  # ensure a,b
        if match is None:
            raise ValueError('nodes should be in the form \'a,b\'')
        one = int(match.group(1))  # get each of a and b
        two = int(match.group(2))
        if one >= self.size or one < 0 or two >= self.size or two < 0:
            raise ValueError('node is out of bounds')


    @staticmethod
    def checkNumber(num):
        """
        Check if num is an integer/float.

        param1: unknown - item to confirm if integer/float
        """

        if not isinstance(num, int) and not isinstance(num, float):
            raise ValueError('number must be an integer/float')


    @staticmethod
    def checkInt(num):
        """
        Check if num is an integer.

        param1: unknown - item to confirm if integer
        """

        if not isinstance(num, int):
            raise ValueError('number must be an integer')


    def getSize(self):
        """
        Return board size.

        return: integer - size of board
        """

        return self.size


    def setWeight(self, u, weight):
        """
        Set incoming edges of vertex u to weight.

        param1: string - node in the form <integer>,<integer>
        param2: integer/float - weight to set
        """

        self.modifyWeightErrorCheck(u, weight)  # comment this out for speed

        if weight < 0: #ensure weight is in bounds
            weight = 0
        elif weight > 100:
            weight = 100

        for edge in self.edges[u]:  # 100 - weight is to unsure higher weights
                                    # correlate to shorter paths when traversing
            edge['weight'] = 100 - float(weight)

        self.dictionary[u] = 100 - float(weight)  # ensure front is highest


    def multiplyWeight(self, u, multiplier):
        """
        Multiply weight of node u by multiplier.

        param1: string - node in the form <integer>,<integer>
        param2: integer/float - number to multiply weight by
        """

        self.modifyWeightErrorCheck(u, multiplier)  # comment this out for speed

        currentWeight = self.getWeight(u)
        self.setWeight(u, currentWeight * multiplier)


    def divideWeight(self, u, divisor):
        """
        Divide weight of node u by divisor.

        param1: string - node in the form <integer>,<integer>
        param2: integer/float - number to divide weight by
        """

        self.modifyWeightErrorCheck(u, divisor)  # comment this out for speed

        currentWeight = self.getWeight(u)
        self.setWeight(u, currentWeight / divisor)


    def addWeight(self, u, addend):
        """
        Increase weight of node u by addend.

        param1: string - node in the form <integer>,<integer>
        param2: integer/float - number to add to weight
        """

        self.modifyWeightErrorCheck(u, addend)  # comment this out for speed

        currentWeight = self.getWeight(u)
        self.setWeight(u, currentWeight + addend)


    def subtractWeight(self, u, subtrahend):
        """
        Decrease weight of node u by subtrahend.

        param1: string - node in the form <integer>,<integer>
        param2: integer/float - number to subtract from weight
        """

        self.modifyWeightErrorCheck(u, subtrahend)  # comment this out for speed

        currentWeight = self.getWeight(u)
        self.setWeight(u, currentWeight - subtrahend)


    def modifyWeightErrorCheck(self, u, num):
        """
        Check weight modification method for errors.

        param1: unknown - item to confirm if node
        param2: unknown - item to confirm if integer/float
        """

        self.checkNode(u)
        self.checkNumber(num)


    def getWeight(self, u):
        """
        Return the weight of the node u from the dictionary.

        param1: string - node in the form <integer>,<integer>
        return: integer/float - weight of node u
        """

        self.checkNode(u)  # comment this out for speed

        return 100 - self.dictionary[u]  # allow human-readable


    def getNodeWithPriority(self, index):
        """
        Return vertex name with priority index.

        param1: int - index to return priority
        return: string - node name with priority index
        """

        self.checkInt(index)  # comment this out for speed

        return self.dictionary.iloc[index:5]


    def getNodesWithPriority(self, start, end):
        """
        Return vertex name with priority index.

        param1: int - start index to return priority
        param2: int - end index to return priority
        return: [string] - node names with priority from start-end
        """

        self.getNodesWithPriorityErrorCheck(start, end)  # comment for speed

        return self.dictionary.iloc[start : end + 1]


    def getNodesWithPriorityErrorCheck(self, start, end):
        """
        Check getNodesWithPriority() for errors.

        param1: int - start index to return priority
        param2: int - end index to return priority
        """

        self.checkInt(start)
        self.checkInt(end)


    def isNodeWeightUnique(self, u):
        """
        Return False if weight appears more than once in the graph.

        param1: string - node to check for duplicate weights
        return: boolean - True if weight is unique, Fale otherwise
        """

        if self.countNodeWeightCopies(u) > 1:
            return False
        return True


    def countNodeWeightCopies(self, u):
        """
        Return False if weight appears more than once in the graph.

        param1: string - node to check for duplicate weights
        return: boolean - True if weight is unique, Fale otherwise
        """

        self.checkNode(u)  # comment this out for speed

        targetWeight = 100 - self.getWeight(u)
        return self.dictionary.values().count(targetWeight)  # occurrences


    def optimumPath(self, u, v):
        """
        Return shortest path between nodes u and v.

        param1,2: string - node in the form <integer>,<integer>
        return: [string] - node names in the optimum path from u to v
        """

        self.optimumPathErrorCheck(u, v)  # comment this out for speed

        vertexIds = self.graph.get_shortest_paths(u, to=v, weights='weight',
                                             mode='OUT', output='vpath')[0]
                                             # generate list of Ids in path
        vertexNames = []
        for vertexId in vertexIds:
            name = self.graph.vs.find(vertexId)['name'] # get human-readable
                                                        # node names
            vertexNames.append(name)

        return vertexNames


    def optimumPathErrorCheck(self, u, v):
        """
        Check optimumPath() method for errors.

        param1,2: unknown - item to confirm if node
        """

        if u == v:
            raise ValueError('u and v cannot be the same node')

        self.checkNode(u)
        self.checkNode(v)


    def show(self, colours, numbers):
        """
        Visualize weights of each node

        param1: boolean - show colours on display?
        param2: boolean - show numbers on display?
        """

        self.showErrorCheck(colours, numbers)  # comment this out for speed

        app = gui('Login Window', '950x950')
        app.setBg('white')
        app.setTitle('SneakySnake Visualiser')

        for row in range(self.size):
            for col in range(self.size):

                nodeName = str(row) + ',' + str(col)
                weight = self.getWeight(nodeName)

                # interpolate square value from gridValue into HSV value
                # between red and green, convert to RGB, convert to hex
                hexCode = '#%02x%02x%02x' % tuple(i * 255 for i in
                            colorsys.hls_to_rgb((weight * 1.2) /
                            float(360), 0.6, 0.8))
                if weight == 0: # color perfect non-valid entries black
                    hexCode = '#000000'
                if weight == 100: # color perfect full-valid entries blue
                    hexCode = '#2196F3'
                if weight > 100 or weight < 0: # color invalid entries grey
                    hexCode = '#616161'

                if numbers: # add numbers
                    app.addLabel(nodeName, weight, col, row)
                else:
                    app.addLabel(nodeName, '', col, row)

                if colours is True: # add colours
                    app.setLabelBg(nodeName, hexCode)

        app.go() # show window


    @staticmethod
    def showErrorCheck(colours, numbers):
        """
        Check show() method for errors.

        param1,2: unknown - item to check if boolean
        """

        if not isinstance(colours, bool):
            raise ValueError('colours must be a boolean')

        if not isinstance(numbers, bool):
            raise ValueError('numbers must be a boolean')



if __name__ == '__main__':
    g = Board(20)
    g.setWeight('0,1', 80)
    g.setWeight('2,2', 100)
    #print g.optimumPath('0,0', '3,5')
    print g.getNodesWithPriority(2, 4)
    print g.isNodeWeightUnique('0,2')
    print g.countNodeWeightCopies('2,2')
    #print g.getWeight('0,1')
    #g.multiplyWeight('2,0', 1)
    #print g.getWeight('2,0')
    #g.sortNames()
    #print g.dictionary
    #g.show(True, True)
