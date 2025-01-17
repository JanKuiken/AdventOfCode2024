"""
Some functions that are multiple times used in AoC 2023
"""

import pprint
from collections import namedtuple, defaultdict

def lines_from_file(file_name):
    """
    Returns a list of lines (with trailing \n removed)
    """
    with open(file_name) as f:
        lines = f.readlines()
        lines = [l.removesuffix('\n') for l in lines]
        return lines

def matrix_from_file(file_name):
    """
    Returns a list (rows) of lists (cols) of chars from a file
    """
    lines = lines_from_file(file_name)
    return [ [ c for c in line ] for line in lines ]

pp = pprint.PrettyPrinter(indent=4, width=120)

def pprint(stuff):
    pp.pprint(stuff)

def print_matrix(matrix):
    for row in matrix:
        for col in row:
            print(col, end='')
        print('\n', end='')

# some named tuples
Point = namedtuple("Point", "x y")
MatrixPoint = namedtuple("MatrixPoint", "row col")


def neighbours(x, y, xmin=0, xmax=100, ymin=0, ymax=100):
    """
    Returns a set of (x,y) tuples
    """
    retval = set()
    for the_x in range(x-1, x+2):
        for the_y in range(y-1, y+2):
            if (     the_x >= xmin
                 and the_x <= xmax
                 and the_y >= ymin
                 and the_y <= ymax ) :
                retval.add((the_x, the_y))
    retval.remove((x,y))
    return retval

def point_neighbours(point, 
                     min_point=Point(0,0), 
                     max_point=Point(100,100)):
                    
    results = neighbours(point.x, 
                         point.y,
                         xmin = min_point.x,
                         xmax = max_point.x,
                         ymin = min_point.y,
                         ymax = max_point.y )

    return set([Point(res[0], res[1]) for res in results])

def matrix_neighbours(matrix_point, 
                      min_matrix_point=MatrixPoint(0,0),
                      max_matrix_point=MatrixPoint(100,100)):
                      
    results = neighbours(matrix_point.row, 
                         matrix_point.col,
                         xmin = min_matrix_point.row,
                         xmax = max_matrix_point.col,
                         ymin = min_matrix_point.row,
                         ymax = max_matrix_point.col )

    return set([MatrixPoint(res[0], res[1]) for res in results])

def numbers_from_str(s):
    """
    Returns a list of integers from a string 
    """
    return [int(i) for i in s.split()]

def split_on_empty_string(list_of_str):
    """
    splits a list of strings in a list of list of strings by empty strings
    """
    retval = [[]]
    for line in list_of_str:
        if line == '':
            retval.append([])
        else:
            retval[-1].append(line)
    return retval

def simple_newton_zero_finding(f, start_x, epsilon = 0.001, dx=0.001):
    """
    pretty naive implementation of Newton's method (do no expect wonders...)
    """
    x = start_x
    while True:
        y = f(x)
        if abs(y) < epsilon:
            return x
        dy = (f(x+dx) - f(x)) / dx
        x  = x - y / dy

def sign(a):
    if a < 0: return -1
    if a > 0: return 1
    return 0

def dijkstra(graph, source):
    """
    i have not used/implemented this alogorithm before, below is the pseudo code 
    from wikipedia. lets change it into Python for our applications...
 
    source: https://en.wikipedia.org/wiki/Dijkstra's_algorithm
    
 1  function Dijkstra(Graph, source):
 2     
 3      for each vertex v in Graph.Vertices:
 4          dist[v] ← INFINITY
 5          prev[v] ← UNDEFINED
 6          add v to Q
 7      dist[source] ← 0
 8     
 9      while Q is not empty:
10          u ← vertex in Q with minimum dist[u]
11          remove u from Q
12         
13          for each neighbor v of u still in Q:
14              alt ← dist[u] + Graph.Edges(u, v)
15              if alt < dist[v]:
16                  dist[v] ← alt
17                  prev[v] ← u
18
19      return dist[], prev[]
"""

     # pseudo code : for each vertex v in Graph.Vertices:
     # pseudo code :     dist[v] ← INFINITY
     # pseudo code :     prev[v] ← UNDEFINED
     # pseudo code :     add v to Q
     # pseudo code : dist[source] ← 0

    vertices = list(graph.keys())
    
    dist = { v: float('infinity') for v in vertices }
    prev = { v: set()  for v in vertices }
    Q = set(vertices)

    dist[source] = 0
    
    # pseudo code : while Q is not empty

    while Q:
    
        # pseudo code : u ← vertex in Q with minimum dist[u]
        min_dist = float('infinity')
        u = None
        for v in Q:
            if dist[v] <= min_dist:
                min_dist = dist[v]
                u = v

        # pseudo code : remove u from Q
        Q.remove(u)
        
        # pseudo code : for each neighbor v of u still in Q:

        neighbours_of_u = graph[u].keys()
        neighbours_of_u_in_Q = [neighbour for neighbour in neighbours_of_u if neighbour in Q]
        for v in neighbours_of_u_in_Q:

            # pseudo code : alt ← dist[u] + Graph.Edges(u, v)
            # pseudo code : if alt < dist[v]:
            # pseudo code :     dist[v] ← alt
            # pseudo code :     prev[v] ← u

            alt = dist[u] + graph[u][v]
            if alt <= dist[v]:
                if alt < dist[v]:
                    prev[v] = set([u])
                else:
                    # alt == dist[v], add a prev instead of replacing it
                    prev[v].add(u)
                dist[v] = alt
        
    # pseudo code : return dist[], prev[]
    return dist, prev

def test_my_dijkstra_function():

    # graph also from https://en.wikipedia.org/wiki/Dijkstra's_algorithm
    graph = defaultdict(dict)
    graph['1'] = {'2':  7, '3':  9, '6': 14         }
    graph['2'] = {'1':  7, '3': 10, '4': 15         }
    graph['3'] = {'1':  9, '2': 10, '4': 11, '6': 2 }
    graph['4'] = {'2': 15, '3': 11, '5':  6         }
    graph['5'] = {'4':  6, '6':  9                  }
    graph['6'] = {'1': 14, '3':  2, '5':  9         }
    for start in graph.keys():
        dist, prev = dijkstra(graph, start)
        print('start', start)
        print('dist', dist)
        print('prev', prev)

class TablePoint:
    """ A minimal class with row,col integers for indexing a table
    operators +,- and *(int) are implemented
    """
    # class variables
    min_row = 0
    max_row = 100
    min_col = 0
    max_col = 100
    
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def isInbounds(self):
        return     self.row >= TablePoint.min_row \
               and self.row <  TablePoint.max_row \
               and self.col >= TablePoint.min_col \
               and self.col <  TablePoint.max_col \
               
    def __repr__(self):
        str_inbounds = ''
        if not self.isInbounds():
            str_inbounds = ' (out of bounds)'
        return 'TablePoint(' + str(self.row) + ', ' + str(self.col) + ')' + str_inbounds

    def __add__(self, other):
        assert isinstance(other, TablePoint), 'Oops, expected a MatrixPoint'
        return TablePoint(self.row + other.row, self.col + other.col)

    def __sub__(self, other):
        assert isinstance(other, TablePoint), 'Oops, expected a MatrixPoint'
        return TablePoint(self.row - other.row, self.col - other.col)

    def __mul__(self, other):
        assert isinstance(other, int), 'Oops, expected an int'
        return TablePoint(self.row * other, self.col * other)

    def __eq__(self, other):
        assert isinstance(other, TablePoint), 'Oops, expected a MatrixPoint'
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

    def neighbours(self):
        result = []
        for row in range(self.row - 1, self.row + 2):
            for col in range(self.col - 1, self.col + 2):
                tp = TablePoint(row, col)
                if tp.isInbounds() and tp != self:
                    result.append(tp)
        return result

    def cartesian_neighbours(self):
        result = []
        tp1 = TablePoint(self.row -1, self.col)
        tp2 = TablePoint(self.row +1, self.col)
        tp3 = TablePoint(self.row, self.col -1)
        tp4 = TablePoint(self.row, self.col +1)
        if tp1.isInbounds(): result.append(tp1)
        if tp2.isInbounds(): result.append(tp2)
        if tp3.isInbounds(): result.append(tp3)
        if tp4.isInbounds(): result.append(tp4)
        return result


# Added first for 2023-day-25, trying to keep it general... but added data member...
#class Graph():
#
#    class Node():
#        def __init__(data=None):
#            self.edges = set()
#            self.data = data
#        def add_edge(node):
#            self.edges.add(node)
#
#    def __init__():
#        graph = {}
#        
#    def add_node(self, key, data=None):
#        # add the node if it doesn't exist:
#        if not key in graph.keys():
#            graph[key] = Node(data)
#
#    def add_edge(self, begin, end, begin_data=None, end_data=None):
#        # add connection in both deirections
#        graph[begin].add(end)
#         graph[end].add(begin)
 






