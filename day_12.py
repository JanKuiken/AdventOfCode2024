"""
Advent of Code 2024, day 12
"""

import aoc_lib as aoc
from collections import defaultdict

matrix = aoc.matrix_from_file("input_12.txt")

# for testing
if False:
    lines = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""".split('\n')
    matrix = [ [ c for c in line ] for line in lines ]

n_rows = len(matrix)
n_cols = len(matrix[0])

aoc.TablePoint.max_row = n_rows
aoc.TablePoint.max_col = n_cols

# we store the fences in a defauldict, key=location, values 'n' and/or 's'....
fences = defaultdict(str)

# matrices for fences to the north, east, south and west of each matrix cell

# set outside perimeter fences
for col in range(n_cols) : fences[aoc.TablePoint(0,col)]        += 'n'
for col in range(n_cols) : fences[aoc.TablePoint(n_rows-1,col)] += 's'
for row in range(n_rows) : fences[aoc.TablePoint(row,0)]        += 'w'
for row in range(n_rows) : fences[aoc.TablePoint(row,n_cols-1)] += 'e'

# set up fences between different gardens (btw double internal fences, but we don't care)
for row in range(n_rows):
    for col in range(n_cols):
        tp = aoc.TablePoint(row,col)
        for neighbour in tp.cartesian_neighbours():
            if matrix[neighbour.row][neighbour.col] != matrix[tp.row][tp.col]:
                delta = neighbour - tp
                if delta.row == -1 : fences[tp] += 'n'
                if delta.row ==  1 : fences[tp] += 's'
                if delta.col == -1 : fences[tp] += 'w'
                if delta.col ==  1 : fences[tp] += 'e'

# recursive function to find all cells of a garden
def find_whole_garden(tp, areas):
    areas.add(tp)
    for neighbour in tp.cartesian_neighbours():
        if not neighbour in areas:
            if matrix[neighbour.row][neighbour.col] == matrix[tp.row][tp.col]:
                areas = find_whole_garden(neighbour, areas)
    return areas

# determine gardens, number of fences and total price
total_price = 0
total_price_part_2 = 0
been_there_done_that = set()
for row in range(n_rows):
    for col in range(n_cols):
        tp = aoc.TablePoint(row,col)
        if tp not in been_there_done_that:
        
            garden = find_whole_garden(tp, set())
            been_there_done_that.update(garden)
            # for part 1            
            n_fences = sum([len(fences[tp2]) for tp2 in garden])
            price = len(garden) * n_fences
            total_price += price            
            # for part 2
            double_count = 0
            for tp2 in garden:
                for neighbour in tp2.cartesian_neighbours():
                    if neighbour in garden:
                        if 's' in fences[neighbour] and 's' in fences[tp2] : double_count += 1
                        if 'n' in fences[neighbour] and 'n' in fences[tp2] : double_count += 1
                        if 'e' in fences[neighbour] and 'e' in fences[tp2] : double_count += 1
                        if 'w' in fences[neighbour] and 'w' in fences[tp2] : double_count += 1
            number_of_sides = n_fences - double_count // 2
            reduced_price = len(garden) * number_of_sides
            total_price_part_2 += reduced_price
            
            #print(tp, matrix[tp.row][tp.col], len(garden), n_fences, price, reduced_price)
           

print("Answer part 1 : ", total_price)

# === Part 2

print("Answer part 2 : ", total_price_part_2)

