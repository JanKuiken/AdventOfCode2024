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

aoc.TablePoint.max_row = len(matrix)
aoc.TablePoint.max_col = len(matrix[0])

# aoc.print_matrix(matrix)

start = None
end   = None
for tp in aoc.TablePoint.iterate():
    if matrix[tp.row][tp.col] == 'S': start = tp
    if matrix[tp.row][tp.col] == 'E': end   = tp

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

# create a graph for dijkstra's algorithm
def create_graph():

    graph = defaultdict(dict)

    def add_all_possible_turns(vertex):
        graph[Vertex(vertex, 'n')][Vertex(vertex, 'e')] = TURN_COST
        graph[Vertex(vertex, 'n')][Vertex(vertex, 'w')] = TURN_COST
        graph[Vertex(vertex, 's')][Vertex(vertex, 'e')] = TURN_COST
        graph[Vertex(vertex, 's')][Vertex(vertex, 'w')] = TURN_COST
        graph[Vertex(vertex, 'e')][Vertex(vertex, 'n')] = TURN_COST
        graph[Vertex(vertex, 'e')][Vertex(vertex, 's')] = TURN_COST
        graph[Vertex(vertex, 'w')][Vertex(vertex, 'n')] = TURN_COST
        graph[Vertex(vertex, 'w')][Vertex(vertex, 's')] = TURN_COST

    
    print('add endpoint in all directions')
    graph[Vertex(end, 'n')] = {}
    graph[Vertex(end, 's')] = {}
    graph[Vertex(end, 'e')] = {}
    graph[Vertex(end, 'w')] = {}

    print('add start point')
    add_all_possible_turns(start)

    print('add turns to the graph')
    for tp1 in aoc.TablePoint.iterate():
        if matrix[tp1.row][tp1.col] in '.SE':
           dirs = []   
           for tp2 in tp1.cartesian_neighbours():
               if matrix[tp2.row][tp2.col] in '.SE':
                   dirs.append(inv_directions[tp2-tp1])
           if (   len(dirs) > 2
               or (len(dirs) == 2 and dirs[0] + dirs[1] in possible_turns)
               or len(dirs) == 1):
                
               # just add all possible turns (don't be cheap)
               add_all_possible_turns(tp1)

    print('add linear moves to the graph')
    for tp1 in aoc.TablePoint.iterate():
        if matrix[tp1.row][tp1.col] in '.SE':
           for tp2 in tp1.cartesian_neighbours():
               if matrix[tp2.row][tp2.col] in '.SE':
                   direction = inv_directions[tp2 - tp1]
                   graph[Vertex(tp1, direction)][Vertex(tp2, direction)] = STEP_COST

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

start = Vertex(start, 'e')

#print('call dijkstra')
#dist, prev = aoc.dijkstra(graph, start)

print('call dijkstra_with_priority_queue')
dist, prev = aoc.dijkstra_with_priority_queue(graph, start)

ends = [Vertex(end, 'n'),
        Vertex(end, 's'),
        Vertex(end, 'e'),
        Vertex(end, 'w'), ]

for e in ends:
    print(e, dist[e])

lowest_score = int(min([dist[e] for e in ends]))

print("Answer part 1 : ", lowest_score)

# === Part 2

walked_path = set()
done = set()
todo = deque([e for e in ends if dist[e]==lowest_score])
while todo:
    vert1 = todo.popleft()
    walked_path.add(vert1.point)
    if not vert1 in done:
        done.add(vert1)
        for vert2 in prev[vert1]:
            todo.append(vert2)

for vert in walked_path:
    matrix[vert.row][vert.col] = 'O'
aoc.print_matrix(matrix)


print("Answer part 2 : ", len(walked_path))

print("\n\nBonus : my dijkstra test function")
aoc.test_my_dijkstra_functions()



