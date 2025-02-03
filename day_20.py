"""
Advent of Code 2024, day 20
"""

import aoc_lib as aoc
from collections import defaultdict, deque
from copy import deepcopy

saving_picoseconds_part_1 = 100
saving_picoseconds_part_2 = 100
matrix = aoc.matrix_from_file("input_20.txt")

# for testing
if False:
    saving_picoseconds_part_1 = 12    # should result in 8, last six lines in example description table
    saving_picoseconds_part_2 = 66    # should result in 67, last six lines in example description table
    lines = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############""".split('\n')
    matrix =  [ [ c for c in line ] for line in lines ]

aoc.TablePoint.max_row = len(matrix)
aoc.TablePoint.max_col = len(matrix[0])

original_matrix = deepcopy(matrix)
aoc.print_matrix(matrix)

start = None
end   = None
for tp in aoc.TablePoint.iterate():
    if matrix[tp.row][tp.col] == 'S': start = aoc.TablePoint(tp.row,tp.col)
    if matrix[tp.row][tp.col] == 'E': end   = aoc.TablePoint(tp.row,tp.col)
print('start', start)
print('end', end)

#create a graph and determine start and end point
def create_graph():
    graph = defaultdict(set)
    for tp1 in aoc.TablePoint.iterate():
        if matrix[tp1.row][tp1.col] in '.SE':
            for tp2 in tp1.cartesian_neighbours():
                if matrix[tp2.row][tp2.col] in '.SE':
                    graph[tp1].add(tp2)
                    graph[tp2].add(tp1)
    return graph

A_LOT = 9999999999
start_to_end = [ [ A_LOT for _ in range(aoc.TablePoint.max_col) ] for _ in range(aoc.TablePoint.max_row) ]
end_to_start = [ [ A_LOT for _ in range(aoc.TablePoint.max_col) ] for _ in range(aoc.TablePoint.max_row) ]

def bfs(graph, start, matrix_to_fill):  # see https://en.wikipedia.org/wiki/Breadth-first_search
    Q = deque()
    seen = set()
    Q.append(start)
    seen.add(start)
    matrix_to_fill[start.row][start.col] = 0
    while Q:
        v = Q.popleft()
        for w in graph[v]:
            if not w in seen:
                matrix_to_fill[w.row][w.col] = matrix_to_fill[v.row][v.col] + 1
                Q.append(w)        
                seen.add(w)

graph = create_graph()
bfs(graph, start, start_to_end)
bfs(graph, end,   end_to_start)
initial_result = start_to_end[end.row][end.col]

def cheat_result(row,col):
    return   2 \
           + min( [ start_to_end[row+1][col],
                    start_to_end[row-1][col],
                    start_to_end[row][col+1],
                    start_to_end[row][col-1] ] )  \
           + min( [ end_to_start[row+1][col],
                    end_to_start[row-1][col],
                    end_to_start[row][col+1],
                    end_to_start[row][col-1] ] ) 

print('initial_result', initial_result)

# take care we change the limits of our TablePoint class
aoc.TablePoint.min_row = 1
aoc.TablePoint.min_col = 1
aoc.TablePoint.max_row = len(matrix) - 1
aoc.TablePoint.max_col = len(matrix[0]) - 1

results = {}
for tp in aoc.TablePoint.iterate():
    if matrix[tp.row][tp.col] == '#':
        r = cheat_result(tp.row, tp.col)
        if r <= initial_result - saving_picoseconds_part_1:
            results[tp] = r

print("Answer part 1 : ", len(results))

# === Part 2

# hmm,.....
#aoc.print_matrix(original_matrix)
# - cheats start with a '#'
# - cheats end with a '.'
# - are at max length 20 (manhatan distance)
# - start and endpoint define a cheat, other equivalent 
#     routes do not count, they are 'the same cheat'
# - there are no muliple cheats

def distance(tp1, tp2):
    return abs(tp1.row - tp2.row) + abs(tp1.col - tp2.col)

# for conviniece (we dont have to check for 'S' and 'E')
matrix[start.row][start.col] = '.'
matrix[end.row][end.col] = '.'

def cheat_result_2(tp1, tp2):
    return start_to_end[tp1.row][tp1.col] + end_to_start[tp2.row][tp2.col] 

def points_within_manhatan_distance(tp, dist):
    for drow in range(-dist, dist+1):
        for dcol in range(-(dist - abs(drow)), (dist - abs(drow))+1):
            tp2 = aoc.TablePoint(tp.row + drow, tp.col + dcol)
            if tp2.isInbounds():
                yield(tp2, abs(drow) + abs(dcol))

results = {}
distance = 20
for tp1 in aoc.TablePoint.iterate():
    if matrix[tp1.row][tp1.col] == '.':
        for tp2, dist in points_within_manhatan_distance(tp1, distance):
            if matrix[tp2.row][tp2.col] == '.':
                r = cheat_result_2(tp1, tp2) + dist
                if r <= initial_result - saving_picoseconds_part_2:
                    results[(tp1, tp2, dist)] = r

print('saving_picoseconds_part_2',saving_picoseconds_part_2)

print("Answer part 2 : ", len(results))
