# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
# This imports everything from `graph.py` as if it was defined in this file!
from graph import * 

#
# Problem 2: Building up the Campus Map
#
# The campus map represents a collection of states (i.e. physical localities),
# as well as ways to change that state and the associated cost (i.e. weighted paths).
#
# That is, the nodes are locations on the map, while the edges are paths to other nodes.
# It is possible to change state from one node to another, but doing so incurs a cost,
# which is represented by the edge chosen from one node to another.
#

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    # TODO
    print("Loading map from file...")
    g = WeightedDigraph()
    pathAndFile = '/home/human/edX/6.00.2x/Python Problem Sets/PS5/ProblemSet5/'+mapFilename
    inFile = open(pathAndFile, 'r')
    for line in inFile:
        edgeAsList = line.split()
        if not g.hasNodeName(edgeAsList[0]):
            g.addNode(Node(edgeAsList[0]))
        if not g.hasNodeName(edgeAsList[1]):
            g.addNode(Node(edgeAsList[1]))
        g.addEdge(WeightedEdge(g.getNode(edgeAsList[0]), g.getNode(edgeAsList[1]), \
                        float(edgeAsList[2]), float(edgeAsList[3])))  
    return g

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors, path = [], shortest = None):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.
    
    This is an exhaustive depth-first search.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)
        path: the path traveled so far (list)
        shortest: the shortest satisfying path seen so far (list)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    assert type(start) == str, "start must be passed to bruteForceSearch as str"
    assert type(end) == str, "end must be passed to bruteForceSearch as str"
    
    startNode = digraph.getNode(start)
    endNode = digraph.getNode(end)
    
    assert digraph.hasNode(startNode), "start node is not in the weighted digraph"
    assert digraph.hasNode(endNode), "end node is not in the weighted digraph"
    path = path + [start]
    if startNode == endNode:
        return path
    for node in digraph.childrenOf(startNode):
        if node.getName() not in path: # To avoid cycles
            newPath = bruteForceSearch(digraph, node.getName(), end,\
                maxTotalDist, maxDistOutdoors, path, shortest)
            if newPath != None \
                and digraph.pathMeetsBothConstraints(newPath, maxTotalDist, \
                    maxDistOutdoors):
                if shortest == None:
                    shortest = newPath
                elif digraph.getTotalDistance(newPath) < \
                    digraph.getTotalDistance(shortest):
                    shortest = newPath                    
    if len(path) == 1 and shortest == None:
        raise ValueError("No path satisfies the constraints")
    else:
        return shortest

#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, route, maxTotalDist, maxDistOutdoors, path = [], shortest = None):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    assert type(start) == str, "start must be passed to bruteForceSearch as str"
    assert type(end) == str, "end must be passed to bruteForceSearch as str"
    
    startNode = digraph.getNode(start)
    endNode = digraph.getNode(end)

    assert digraph.hasNode(startNode), "start node is not in the weighted digraph"
    assert digraph.hasNode(endNode), "end node is not in the weighted digraph"
    path = path + [start]
    route.addStep()
    printPath(path, "DFS")
    if startNode == endNode:
        return path
    if not digraph.hasChildNodes(startNode):
        print("No children, marking dead node")
        route.markNodeDead(start)
    for node in digraph.childrenOf(startNode):
        if not route.isDeadNode(node.getName()):
            break
    else:
        print("No non-dead children nodes, marking dead node")
        route.markNodeDead(start)
        return shortest
    for node in digraph.childrenOf(startNode):
        if shortest == None or \
            digraph.getTotalDistance(path) < digraph.getTotalDistance(shortest):
            if (node.getName() not in path) and (not route.isDeadNode(node.getName())): # To avoid cycles
                newPath = directedDFS(digraph, node.getName(), end, route,\
                    maxTotalDist, maxDistOutdoors, path, shortest)
                if newPath != None \
                    and digraph.pathMeetsBothConstraints(newPath, maxTotalDist, \
                        maxDistOutdoors):
                    if shortest == None:
                        shortest = newPath
                    elif digraph.getTotalDistance(newPath) < \
                        digraph.getTotalDistance(shortest):
                        shortest = newPath                    
    if len(path) == 1 and shortest == None:
        raise ValueError("No path satisfies the constraints")
    else:
        return shortest
    
def bruteForcePruneSearch(digraph, start, end, route, maxTotalDist, maxDistOutdoors, path = [], shortest = None):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.
    
    This is an exhaustive depth-first search.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)
        path: the path traveled so far (list)
        shortest: the shortest satisfying path seen so far (list)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    assert type(start) == str, "start must be passed to bruteForceSearch as str"
    assert type(end) == str, "end must be passed to bruteForceSearch as str"
    
    startNode = digraph.getNode(start)
    endNode = digraph.getNode(end)
    
    assert digraph.hasNode(startNode), "start node is not in the weighted digraph"
    assert digraph.hasNode(endNode), "end node is not in the weighted digraph"
    route.addStep()
    path = path + [start]
    printPath(path, "Prune")
    if startNode == endNode:
        return path
    if not digraph.hasChildNodes(startNode):
        print("No children, marking dead node")
        route.markNodeDead(start)
    for node in digraph.childrenOf(startNode):
        if not route.isDeadNode(node.getName()):
            break
    else:
        print("No non-dead children nodes, marking dead node")
        route.markNodeDead(start)
        return shortest
    for node in digraph.childrenOf(startNode):
        if (node.getName() not in path) and (not route.isDeadNode(node.getName())): # To avoid cycles
            newPath = bruteForcePruneSearch(digraph, node.getName(), end, route,\
                maxTotalDist, maxDistOutdoors, path, shortest)
            if newPath != None \
                and digraph.pathMeetsBothConstraints(newPath, maxTotalDist, \
                    maxDistOutdoors):
                if shortest == None:
                    shortest = newPath
                elif digraph.getTotalDistance(newPath) < \
                    digraph.getTotalDistance(shortest):
                    shortest = newPath                    
    if len(path) == 1 and shortest == None:
        raise ValueError("No path satisfies the constraints")
    else:
        return shortest
    


#### NOTE! These tests may take a few minutes to run!! ####
if __name__ == '__main__':
    ## Test cases
    mitMap = load_map("mit_map.txt")
    print(isinstance(mitMap, Digraph))
    print(isinstance(mitMap, WeightedDigraph))
    print('nodes', mitMap.nodes)
    print('edges', mitMap.edges)
    LARGE_DIST = 1000000
    
    # Uncomment below when ready to test
    
    #~ User Test case A
    #~ path = [mitMap.getNode('32'), mitMap.getNode('76'), mitMap.getNode('68')]
    #~ print(mitMap.getOutdoorDistance(path))

    #~ Course Test: map2 B
    #~ map2 = load_map("map2.txt")
    #~ print(bruteForceSearch(map2, "1", "3", 18, 18))
    #~ print(bruteForceSearch(map2, "1", "3", 15, 15))
    #~ print(bruteForceSearch(map2, "1", "3", 18, 0))
    #~ print(bruteForceSearch(map2, "1", "3", 10, 10))
    
    #~ Course Test: map3 B
    #~ map3 = load_map("map3.txt")
    #~ print(bruteForceSearch(map3, "1", "3", 18, 18))
    #~ print(bruteForceSearch(map3, "1", "3", 18, 0))
    #~ print(bruteForceSearch(map3, "1", "3", 10, 10))

    #~ Course Test: map5 B
    #~ map5 = load_map("map5.txt")
    #~ print(bruteForceSearch(map5, "1", "3", 17, 8))
    #~ ['1', '2', '4', '3']
    #~ print(bruteForceSearch(map5, "1", "5", 23, 11))
    #~ ['1', '2', '4', '3', '5']
    #~ print(bruteForceSearch(map5, "4", "5", 21, 11))
    #~ ['4', '3', '5']
    #~ print(bruteForceSearch(map5, "5", "1", 100, 100))
    #~ ValueError successfully raised
    #~ print(bruteForceSearch(map5, "4", "5", 8, 2))
    #~ ValueError successfully raised

    #~ Course Test: map6 B
    #~ map6 = load_map("map6.txt")
    #~ print(bruteForceSearch(map6, "1", "5", 35, 9))
    #~ print(bruteForceSearch(map6, "1", "5", 35, 8))
    #~ print(bruteForceSearch(map6, "4", "5", 21, 11))
    #~ print(bruteForceSearch(map6, "4", "5", 21, 1))
    #~ print(bruteForceSearch(map6, "4", "5", 19, 1))
    #~ print(bruteForceSearch(map6, "3", "2", 100, 100))
    #~ print(bruteForceSearch(map6, "4", "5", 8, 2))
    #~ ['1', '2', '4', '3', '5']
    #~ ['1', '2', '4', '5']
    #~ ['4', '3', '5']
    #~ ['4', '5']
    #~ ValueError successfully raised
    #~ ValueError successfully raised
    #~ ValueError successfully raised

    #~ Test case 1
    #~ print("---------------")
    #~ print("Test case 1:")
    #~ print("Find the shortest-path from Building 32 to 56")
    #~ expectedPath1 = ['32', '56']
    #~ route = Path('32', '56')
    #~ brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    #~ dfsPath1 = directedDFS(mitMap, '32', '56', route, LARGE_DIST, LARGE_DIST)
    #~ prunePath1 = bruteForcePruneSearch(mitMap, '32', '56', route, LARGE_DIST, LARGE_DIST)
    #~ print("Expected: ", expectedPath1)
    #~ print("Brute-force: ", brutePath1)
    #~ print("DFS: ", dfsPath1)
    #~ print("PrunePath: ", prunePath1)
    #~ print("Dead nodes: ", route.getDeadNodes())
    #~ print("Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1))

    #~ Test case 2
    #~ print("---------------")
    #~ print("Test case 2:")
    #~ print("Find the shortest-path from Building 32 to 56 without going outdoors")
    #~ expectedPath2 = ['32', '36', '26', '16', '56']
    #~ brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
    #~ dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
    #~ print("Expected: ", expectedPath2)
    #~ print("Brute-force: ", brutePath2)
    #~ print("DFS: ", dfsPath2)
    #~ print("Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2))

    #~ Test case 3
    #~ print("---------------")
    #~ print("Test case 3:")
    #~ print("Find the shortest-path from Building 2 to 9")
    #~ expectedPath3 = ['2', '3', '7', '9']
    #~ brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    #~ dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    #~ print("Expected: ", expectedPath3)
    #~ print("Brute-force: ", brutePath3)
    #~ print("DFS: ", dfsPath3)
    #~ print("Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3))

    #~ Test case 4
    #~ print("---------------")
    #~ print("Test case 4:")
    #~ print("Find the shortest-path from Building 2 to 9 without going outdoors")
    #~ expectedPath4 = ['2', '4', '10', '13', '9']
    #~ brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
    #~ dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
    #~ print("Expected: ", expectedPath4)
    #~ print("Brute-force: ", brutePath4)
    #~ print("DFS: ", dfsPath4)
    #~ print("Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4))

    #~ Test case 5
    #~ print("---------------")
    #~ print("Test case 5:")
    #~ print("Find the shortest-path from Building 1 to 32")
    #~ expectedPath5 = ['1', '4', '12', '32']
    #~ route1 = Path()
    #~ route2 = Path()
    #~ brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
    #~ prunePath5 = bruteForcePruneSearch(mitMap, '1', '32', route1, LARGE_DIST, LARGE_DIST)
    #~ dfsPath5 = directedDFS(mitMap, '1', '32', route2, LARGE_DIST, LARGE_DIST)
    #~ print("Expected: ", expectedPath5)
    #~ print("Brute-force: ", brutePath5)
    #~ print("Prune: ", prunePath5)
    #~ print(route1.getDeadNodes(), route1.getSteps())
    #~ print("DFS: ", dfsPath5)
    #~ print(route2.getDeadNodes(), route2.getSteps())
    #~ print("Correct? BFS: {0}; DFS: {1}, Prune: {2}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5, \
    #~ expectedPath5 == prunePath5))

    #~ Test case 6
    #~ print("---------------")
    #~ print("Test case 6:")
    #~ print("Find the shortest-path from Building 1 to 32 without going outdoors")
    #~ expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
    #~ brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
    #~ route1 = Path()
    #~ prunePath6 = bruteForcePruneSearch(mitMap, '1', '32', route1, LARGE_DIST, 0)
    #~ route2 = Path()
    #~ dfsPath6 = directedDFS(mitMap, '1', '32', route2, LARGE_DIST, 0)
    #~ print("Expected: ", expectedPath6)
    #~ print("Brute-force: ", brutePath6)
    #~ print("Prune: ", prunePath6)
    #~ print("DFS: ", dfsPath6)
    #~ print(route1.getDeadNodes(), route1.getSteps())
    #~ print(route2.getDeadNodes(), route2.getSteps())
    #~ print("Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6))

    #~ Test case 7
    #~ print("---------------")
    #~ print("Test case 7:")
    #~ print("Find the shortest-path from Building 8 to 50 without going outdoors")
    #~ bruteRaisedErr = 'No'
    #~ pruneRaisedErr = 'No'
    #~ dfsRaisedErr = 'No'
    
    
    #~ try:
        #~ bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
    #~ except ValueError:
        #~ bruteRaisedErr = 'Yes'
    #~ route1 = Path('8','50')
    #~ try:
        #~ bruteForcePruneSearch(mitMap, '8', '50', route1, LARGE_DIST, 0)
    #~ except ValueError:
        #~ pruneRaisedErr = 'Yes'
    
    #~ route2 = Path('8','50')
    #~ try:
        #~ directedDFS(mitMap, '8', '50', route2, LARGE_DIST, 0)
    #~ except ValueError:
        #~ dfsRaisedErr = 'Yes'

    #~ print(route1.getDeadNodes(), route1.getSteps())
    #~ print(route2.getDeadNodes(), route2.getSteps())
    
    #~ print("Expected: No such path! Should throw a value error.")
    #~ print("Did brute force search raise an error?", bruteRaisedErr)
    #~ print("Did brute force prune search raise an error?", pruneRaisedErr)
    #~ print("Did DFS search raise an error?", dfsRaisedErr)

    #~ Test case 8
    #~ print("---------------")
    #~ print("Test case 8:")
    #~ print("Find the shortest-path from Building 10 to 32 without walking")
    #~ print("more than 100 meters in total")
    #~ bruteRaisedErr = 'No'
    #~ dfsRaisedErr = 'No'
    #~ try:
        #~ bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
    #~ except ValueError:
        #~ bruteRaisedErr = 'Yes'
    
    #~ try:
        #~ directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
    #~ except ValueError:
        #~ dfsRaisedErr = 'Yes'
    
    #~ print("Expected: No such path! Should throw a value error.")
    #~ print("Did brute force search raise an error?", bruteRaisedErr)
    #~ print("Did DFS search raise an error?", dfsRaisedErr)
