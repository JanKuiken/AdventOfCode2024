"""
Advent of Code 2024, day 8
"""

import aoc_lib as aoc

from collections import defaultdict
from string import ascii_letters, digits
from itertools import combinations, permutations

matrix = aoc.matrix_from_file("input_08.txt")

# for testing
if False:
    lines = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............""".split('\n')
    matrix = [ [ c for c in line ] for line in lines ]


n_rows = len(matrix)
n_cols = len(matrix[0])

aoc.TablePoint.max_row = n_rows
aoc.TablePoint.max_col = n_cols

frequencies = defaultdict(list)
for row in range(n_rows):
    for col in range(n_cols):
        if matrix[row][col] in ascii_letters + digits:
            frequencies[matrix[row][col]].append(aoc.TablePoint(row,col))

antinodes = set()
for frequency in frequencies.keys():
    locations = frequencies[frequency]
    for combo in combinations(locations,2):
        for antenna_1, antenna_2 in permutations(combo):
            delta = antenna_2 - antenna_1
            antinode = antenna_2 + delta
            if antinode.isInbounds():
                antinodes.add(antinode)

for antidode in antinodes:
    matrix[antidode.row][antidode.col] = '#'

aoc.print_matrix(matrix)

count = 0
for row in range(n_rows):
    for col in range(n_cols):
        if matrix[row][col] == '#':
            count += 1
print('count : ', count)

print("Answer part 1 : ", len(antinodes))


# === Part 2

antinodes = set()
for frequency in frequencies.keys():
    locations = frequencies[frequency]
    for combo in combinations(locations,2):
        for antenna_1, antenna_2 in permutations(combo):
            delta = antenna_2 - antenna_1
            for i in range(50):
                antinode = antenna_2 + delta * i
                if antinode.isInbounds():
                    antinodes.add(antinode)

print("Answer part 2 : ", len(antinodes))


antinodes = set()
for frequency in frequencies.keys():
    locations = frequencies[frequency]
    for combo in combinations(locations,2):
        for antenna_1, antenna_2 in permutations(combo):
            delta = antenna_2 - antenna_1
            antinode = antenna_2 + delta
            while antinode.isInbounds():
                antinodes.add(antinode)
                antinode = antinode + delta

print("Answer part 2b : ", len(antinodes))






