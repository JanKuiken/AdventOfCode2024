"""
Advent of Code 2024, day 10
"""

import aoc_lib as aoc

from collections import defaultdict

matrix = aoc.matrix_from_file("input_10.txt")

# for testing
if False:
    lines = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""".split('\n')
    matrix = [ [ c for c in line ] for line in lines ]

n_rows = len(matrix)
n_cols = len(matrix[0])

# cast matrix to ints
for row in range(n_rows):
    for col in range(n_cols):
        matrix[row][col] = int(matrix[row][col])

aoc.TablePoint.max_row = n_rows
aoc.TablePoint.max_col = n_cols

graph = defaultdict(list)
for row in range(n_rows):
    for col in range(n_cols):
        tp = aoc.TablePoint(row,col)
        for neighbour in tp.cartesian_neighbours():
            if matrix[neighbour.row][neighbour.col] == matrix[tp.row][tp.col] + 1:
                graph[tp].append(neighbour)

# aoc.pprint(graph)

start_tp = None
trails_found_set= defaultdict(set)
trails_found_list= defaultdict(list)

def find_a_nine(tp):
    global trails_found
    if matrix[tp.row][tp.col] == 9:
        trails_found_set[start_tp].add(tp)
        trails_found_list[start_tp].append(tp)
        return
    for next_tp in graph[tp]:
        find_a_nine(next_tp)

for row in range(n_rows):
    for col in range(n_cols):
        tp = aoc.TablePoint(row,col)
        start_tp = tp
        if matrix[tp.row][tp.col] == 0:
            been_there_done_that = []
            find_a_nine(tp)

# aoc.pprint(trails_found)
nines_found = sum(map(len, trails_found_set.values()))

print("Answer part 1 : ", nines_found)

# === Part 2

nines_found = sum(map(len, trails_found_list.values()))

print("Answer part 2 : ", nines_found)



