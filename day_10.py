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

aoc.TablePoint.max_row = len(matrix)
aoc.TablePoint.max_col = len(matrix[0])

# change matrix chars to ints
for tp in aoc.TablePoint.iterate():
    matrix[tp.row][tp.col] = int(matrix[tp.row][tp.col])

# make a graph of possible moves
graph = defaultdict(list)
for tp in aoc.TablePoint.iterate():
    for neighbour in tp.cartesian_neighbours():
        if matrix[neighbour.row][neighbour.col] == matrix[tp.row][tp.col] + 1:
            graph[tp].append(neighbour)

# my global variables (besides graph)
start_tp = None
trails_found_set= set()
trails_found_list= list()

def find_a_nine(tp):
    if matrix[tp.row][tp.col] == 9:
        trails_found_set.add((start_tp,tp))
        trails_found_list.append((start_tp,tp))
    else:
        for next_tp in graph[tp]:
            find_a_nine(next_tp)

for tp in aoc.TablePoint.iterate():
    if matrix[tp.row][tp.col] == 0:
        start_tp = tp
        find_a_nine(tp)

aoc.print_matrix(matrix)

print("Answer part 1 : ", len(trails_found_set))

# === Part 2

print("Answer part 2 : ", len(trails_found_list))

