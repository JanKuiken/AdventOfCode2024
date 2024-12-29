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

n_rows = len(matrix)
n_cols = len(matrix[0])

aoc.TablePoint.max_row = n_rows
aoc.TablePoint.max_col = n_cols

original_matrix = deepcopy(matrix)
aoc.print_matrix(matrix)

start = None
end   = None
for row in range(n_rows):
    for col in range(n_cols):
        if matrix[row][col] == 'S': start = aoc.TablePoint(row,col)
        if matrix[row][col] == 'E': end   = aoc.TablePoint(row,col)
print('start', start)
print('end', end)

#create a graph and determine start and end point
def create_graph():
    graph = defaultdict(set)
    for row in range(n_rows):
        for col in range(n_cols):
            tp1 = aoc.TablePoint(row,col)
            if matrix[row][col] in '.SE':
                for tp2 in tp1.cartesian_neighbours():
                    if matrix[tp2.row][tp2.col] in '.SE':
                        graph[tp1].add(tp2)
                        graph[tp2].add(tp1)
    return graph

A_LOT = 9999999999
start_to_end = [ [ A_LOT for _ in range(n_cols) ] for _ in range(n_rows) ]
end_to_start = [ [ A_LOT for _ in range(n_cols) ] for _ in range(n_rows) ]

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

results = {}
for row in range(1, n_rows-1):
    for col in range(1, n_cols-1):
        if matrix[row][col] == '#':
            r = cheat_result(row,col)
            if r <= initial_result - saving_picoseconds_part_1:
                results[(row,col)] = r

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

def distance(row1, col1, row2, col2):
    return abs(row1 - row2) + abs(col1 - col2)

# for conviniece (we dont have to check for 'S' and 'E')
matrix[start.row][start.col] = '.'
matrix[end.row][end.col] = '.'

def cheat_result_2(row1, col1, row2, col2):
    return start_to_end[row1][col1] + end_to_start[row2][col2] 

# we need an aweful lots of idents....
results = {}
for row1 in range(1, n_rows-1):
    for col1 in range(1, n_cols-1):
        if matrix[row1][col1] == '.':
            for row2 in range(1, n_rows-1):
                for col2 in range(1, n_cols-1):
                    if matrix[row2][col2] == '.':
                        dist = distance(row1, col1, row2, col2)
                        if dist <= 20:
                            r = cheat_result_2(row1, col1, row2, col2) + dist 
                            if r <= initial_result - saving_picoseconds_part_2:
                                results[(row1, col1, row2, col2, dist)] = r

print('saving_picoseconds_part_2',saving_picoseconds_part_2)

print("Answer part 2 : ", len(results))
