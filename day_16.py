"""
Advent of Code 2024, day 16
"""

import aoc_lib as aoc
from collections import defaultdict, deque, namedtuple
from itertools import combinations
from copy import deepcopy

matrix = aoc.matrix_from_file("input_16.txt")

# for testing
if False:
    lines = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############""".split('\n')
    matrix =  [ [ c for c in line ] for line in lines ]

# my even smaller test...
if False:
    lines = """#####
#..E#
#.###
#S..#
#####""".split('\n')
    matrix =  [ [ c for c in line ] for line in lines ]

# the bigger example...
if False:
    lines = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################""".split('\n')
    matrix =  [ [ c for c in line ] for line in lines ]

n_rows = len(matrix)
n_cols = len(matrix[0])

aoc.TablePoint.max_row = n_rows
aoc.TablePoint.max_col = n_cols

aoc.print_matrix(matrix)

start = None
end   = None
for row in range(n_rows):
    for col in range(n_cols):
        if matrix[row][col] == 'S': start = aoc.TablePoint(row,col)
        if matrix[row][col] == 'E': end   = aoc.TablePoint(row,col)
print('start', start)
print('end', end)

# we have cheap 'normal' steps and expensive 'turns'
# probably each turn is more expensive then all 'normal' steps.
# perhaps we only need to consider the 'corners'
# .. nwaah, don't bother, we'll gonna use power tools:

# Googling 'traversing weighted graph' pointed me to Edsger...
# https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

directions = { 'n' : aoc.TablePoint(-1, 0),
               's' : aoc.TablePoint( 1, 0),
               'e' : aoc.TablePoint( 0, 1),
               'w' : aoc.TablePoint( 0,-1), }

inv_directions = { aoc.TablePoint(-1, 0) : 'n',
                   aoc.TablePoint( 1, 0) : 's',
                   aoc.TablePoint( 0, 1) : 'e',
                   aoc.TablePoint( 0,-1) : 'w', }

opposite_direction = { 'n' : 's', 
                       's' : 'n', 
                       'e' : 'w', 
                       'w' : 'e', }

possible_turns = ['ne', 'nw', 'se', 'sw', 'en', 'es', 'wn', 'ws']


Vertex = namedtuple('Vertex', 'point direction')
                
TURN_COST = 1000
STEP_COST = 1

def cost_of_move(vert1, vert2):
    """ Retrun the cost of a move, if the move is not possible return -1"""
    # first filter as many as possible
    if vert1.point == vert2.point:                                     return -1
    if vert1.direction != vert2.direction:                             return -1
    if vert1.direction == 'n'  and vert2.point.row >= vert1.point.row: return -1
    if vert1.direction == 's'  and vert2.point.row <= vert1.point.row: return -1
    if vert1.direction == 'e'  and vert2.point.col <= vert1.point.col: return -1
    if vert1.direction == 'w'  and vert2.point.col >= vert1.point.col: return -1
    if vert1.direction in 'ns' and vert1.point.col != vert2.point.col: return -1 
    if vert1.direction in 'ew' and vert1.point.row != vert2.point.row: return -1
    if vert1.direction in 'ns' : dist = abs(vert2.point.row - vert1.point.row)
    if vert1.direction in 'ew' : dist = abs(vert2.point.col - vert1.point.col)
    # almost there, we only have to check if we don't encounter a '#' from vert1 to vert2...
    for i in range(1,dist):
        tp = vert1.point + directions[vert1.direction] * i
        if matrix[tp.row][tp.col] == '#':
            return -1  
    # we're done
    return dist * STEP_COST

# create a graph for dijkstra's algorithm
def create_graph():

    graph = defaultdict(dict)
    
    print('add endpoint in all directions')
    graph[Vertex(end, 'n')] = {}
    graph[Vertex(end, 's')] = {}
    graph[Vertex(end, 'e')] = {}
    graph[Vertex(end, 'w')] = {}

    print('add start point with all possible turns (don\'t be cheap)')
    graph[Vertex(start, 'n')][Vertex(start, 'e')] = 1000        
    graph[Vertex(start, 'n')][Vertex(start, 'w')] = 1000        
    graph[Vertex(start, 's')][Vertex(start, 'e')] = 1000        
    graph[Vertex(start, 's')][Vertex(start, 'w')] = 1000        
    graph[Vertex(start, 'e')][Vertex(start, 'n')] = 1000        
    graph[Vertex(start, 'e')][Vertex(start, 's')] = 1000        
    graph[Vertex(start, 'w')][Vertex(start, 'n')] = 1000        
    graph[Vertex(start, 'w')][Vertex(start, 's')] = 1000        

    print('add turns to the graph')
    for row in range(n_rows):
        for col in range(n_cols):
            if matrix[row][col] in '.SE':
                tp1 = aoc.TablePoint(row,col)
                dirs = []
                for tp2 in tp1.cartesian_neighbours():
                    if matrix[tp2.row][tp2.col] in '.SE':
                        dirs.append(inv_directions[tp2-tp1])
                if (   len(dirs) > 2
                    or (len(dirs) == 2 and dirs[0] + dirs[1] in possible_turns)):
                    
                    # just add all possible turns (don't be cheap)
                    graph[Vertex(tp1, 'n')][Vertex(tp1, 'e')] = 1000        
                    graph[Vertex(tp1, 'n')][Vertex(tp1, 'w')] = 1000        
                    graph[Vertex(tp1, 's')][Vertex(tp1, 'e')] = 1000        
                    graph[Vertex(tp1, 's')][Vertex(tp1, 'w')] = 1000        
                    graph[Vertex(tp1, 'e')][Vertex(tp1, 'n')] = 1000        
                    graph[Vertex(tp1, 'e')][Vertex(tp1, 's')] = 1000        
                    graph[Vertex(tp1, 'w')][Vertex(tp1, 'n')] = 1000        
                    graph[Vertex(tp1, 'w')][Vertex(tp1, 's')] = 1000

    print('add linear moves to the graph')
    for vert1 in graph.keys():
        for vert2 in graph.keys():
            cost = cost_of_move(vert1, vert2)
            if cost > 0:
                graph[vert1][vert2] = cost 

    print('that\'s about that, we have a graph')
    return graph

def short_vertex(vert):
    return f'{vert.point.row}, {vert.point.col}, {vert.direction}'

def print_graph():
    for vert1 in graph.keys():
        print(short_vertex(vert1))
        for vert2,cost in graph[vert1].items():
            print(f'    {short_vertex(vert2)} : {cost}')

graph = create_graph()
# print_graph()

print('call dijkstra')
start = Vertex(start, 'e')
dist, prev = aoc.dijkstra(graph, start)

ends = [Vertex(end, 'n'),
        Vertex(end, 's'),
        Vertex(end, 'e'),
        Vertex(end, 'w'), ]

for e in ends:
    print(e, dist[e])

lowest_score = min([dist[e] for e in ends])

print("Answer part 1 : ", lowest_score)

# === Part 2

print("Answer part 2 : ", )

