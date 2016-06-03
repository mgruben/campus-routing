# 6.00.2x Problem Set 5
# Graph optimization
#
# A set of data structures to represent graphs
#

class Node(object):
    def __init__(self, name):
        self.name = str(name)
    def getName(self):
        return self.name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return self.name == other.name
    def __ne__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        # Override the default hash method
        # Think: Why would we want to do this?
        return self.name.__hash__()

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __str__(self):
        return '{0}->{1}'.format(self.src, self.dest)


class WeightedEdge(Edge):
    def __init__(self, src, dest, totalDistance = 1.0, outdoorDistance = 1.0):
        Edge.__init__(self, src, dest)
        self.totalDistance = totalDistance
        self.outdoorDistance = outdoorDistance
    def getTotalDistance(self):
        return self.totalDistance
    def getOutdoorDistance(self):
        return self.outdoorDistance
    def __str__(self):
        return str(self.src) + '->' + str(self.dest) +' ('\
            + str(self.totalDistance) + ', ' + str(self.outdoorDistance) + ')'

class Digraph(object):
    """
    A directed graph
    """
    def __init__(self):
        # A Python Set is basically a list that doesn't allow duplicates.
        # Entries into a set must be hashable (where have we seen this before?)
        # Because it is backed by a hashtable, lookups are O(1) as opposed to the O(n) of a list (nifty!)
        # See http://docs.python.org/2/library/stdtypes.html#set-types-set-frozenset
        self.nodes = set([])
        self.edges = {}
    def addNode(self, node):
        if node in self.nodes:
            # Even though self.nodes is a Set, we want to do this to make sure we
            # don't add a duplicate entry for the same node in the self.edges list.
            raise ValueError('Duplicate node')
        else:
            self.nodes.add(node)
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.nodes
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = '{0}{1}->{2}\n'.format(res, k, d)
        return res[:-1]
        
class WeightedDigraph(Digraph):
    """
    A directed graph allowing for edge weights
    """
    def __init__(self):
        self.nodes = set([])
        self.nodeTable = {} ## stores nodeName:Node pairs
        self.edges = {}
        self.edgeTable = {} ## stores (sourceNode, destNode):Edge pairs
    def addEdge(self, edge):  ## Note that the problem expects weights to be
                              ## a tuple of floats, but that the destination node
                              ## should not be included in this tuple; rather dest
                              ## should be a standalone integer.
                              ## Both dest and (tot, outs), should be in their own
                              ## list.
                              ## Thus, [dest, (tot, outs)]
        src = edge.getSource()
        dest = edge.getDestination()
        tot = edge.getTotalDistance()
        outs = edge.getOutdoorDistance()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append([dest, (tot, outs)])
        self.edgeTable[(src,dest)] = edge
    def getEdge(self, src, dest):
        return self.edgeTable[(src, dest)]
    def addNode(self, node):
        if node in self.nodes:
            raise ValueError("Duplicate node")
        else:
            self.nodes.add(node)
            self.nodeTable[node.getName()] = node
            self.edges[node] = []
    def getNode(self, nodeName):
        return self.nodeTable[nodeName]            
    def hasNode(self, node):
        return node in self.nodes
    def hasNodeName(self, nodeName):
        return nodeName in self.nodeTable
    def childrenOf(self, node):
        children = []
        for entry in self.edges[node]:
            children.append(entry[0])
        return children
    def getTotalDistance(self, path):
        total = 0
        for i in range(len(path) - 1):
            total += self.getEdge(path[i], path[i+1]).getTotalDistance()
        return total
    def getOutdoorDistance(self, path):
        outdoors = 0
        for i in range(len(path) - 1):
            outdoors += self.getEdge(path[i], path[i+1]).getTotalDistance()
        return outdoors
    def __str__(self):
        res = ''
        for k in self.edges:
            for d in self.edges[k]:
                res = '{0}{1}->{2} ({3}, {4})\n'.format(res, k, d[0], d[1][0], d[1][1])
        return res[:-1]

def printPath(path):
    # a path is a list of nodes
    result = ''
    for i in range(len(path)):
        if i == len(path) - 1:
            result = result + str(path[i])
        else:
            result = result + str(path[i]) + '->'
    return result

#~ g = WeightedDigraph()
#~ na = Node('a')
#~ nb = Node('b')
#~ nc = Node('c')
#~ g.addNode(na)
#~ g.addNode(nb)
#~ g.addNode(nc)
#~ e1 = WeightedEdge(na, nb, 15, 10)
#~ print(e1)
#~ print(e1.getTotalDistance())
#~ print(e1.getOutdoorDistance())
#~ e2 = WeightedEdge(na, nc, 14, 6)
#~ e3 = WeightedEdge(nb, nc, 3, 1)
#~ print(e2)
#~ print(e3)
#~ g.addEdge(e1)
#~ g.addEdge(e2)
#~ g.addEdge(e3)
#~ print(g)
