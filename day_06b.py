"""
Advent of Code 2024, day 6
"""

import aoc_lib as aoc
from copy import deepcopy
from collections import defaultdict

matrix = aoc.matrix_from_file("input_06.txt")

# for testing
if False:
    lines = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""".split('\n')
    matrix = [ [ c for c in line ] for line in lines ]


origional_matrix = deepcopy(matrix)

n_rows = len(matrix)
n_cols = len(matrix[0])

# find start position (we use a tuple (row,col) as position
for row in range(n_rows):
    for col in range(n_cols):
        if matrix[row][col] == '^':
            pos = row, col
start_pos = pos

direction = (-1,0)
right_turn = { (-1, 0) : ( 0, 1),
               ( 0, 1) : ( 1, 0),
               ( 1, 0) : ( 0,-1),
               ( 0,-1) : (-1, 0)  }


# we're gonna use global variables as much as possible...
def next_pos():
    return (pos[0] + direction[0], pos[1] + direction[1])

def on_map(pos):
    return pos[0] >= 0 and pos[0] < n_rows and  pos[1] >= 0 and pos[1] < n_cols

def char_on_map(pos):
    if on_map(pos): return matrix[pos[0]][pos[1]]
    
def mark_map(pos, char):
    matrix[pos[0]][pos[1]] = char

while on_map(pos):
    if char_on_map(next_pos()) == '#':
        direction = right_turn[direction]
    else:
        mark_map(pos, 'X')
        pos = next_pos()

aoc.print_matrix(matrix)

count = 0
for row in range(n_rows):
    for col in range(n_cols):
        if matrix[row][col] == 'X':
            count += 1

print("Answer part 1 : ", count)


# === Part 2

blockers = set()

for row in range(n_rows):
    print(row)
    for col in range(n_cols):

        testpos = (row, col)
        matrix = deepcopy(origional_matrix)
        if char_on_map(testpos) == '.':
            mark_map(testpos, '#')     # covers also the startpos, because it's a '^'
                
        pos = start_pos
        direction = (-1,0)
        been_there_done_that = defaultdict(list)


        circular = False
        while on_map(pos):
            if char_on_map(next_pos()) == '#':
                direction = right_turn[direction]
            else:
                mark_map(pos, 'X')
                if direction in been_there_done_that[pos]:
                    circular = True
                    blockers.add(testpos)
                    break        
                been_there_done_that[pos].append(direction)
                pos = next_pos()

print("Answer part 2 : ", len(blockers))

