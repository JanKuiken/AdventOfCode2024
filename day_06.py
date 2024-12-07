"""
Advent of Code 2024, day 6
"""

import aoc_lib as aoc

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


n_rows = len(matrix)
n_cols = len(matrix[0])

# find start position (we use a tuple (row,col) as position
for row in range(n_rows):
    for col in range(n_cols):
        if matrix[row][col] == '^':
            pos = row, col

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
    
def mark_map(pos):
    matrix[pos[0]][pos[1]] = 'X'

while on_map(pos):
    if char_on_map(next_pos()) == '#':
        direction = right_turn[direction]
    else:
        mark_map(pos)
        pos = next_pos()

aoc.print_matrix(matrix)

count = 0
for row in range(n_rows):
    for col in range(n_cols):
        if matrix[row][col] == 'X':
            count += 1

print("Answer part 1 : ", count)


# === Part 2

print("Answer part 2 : ", )

