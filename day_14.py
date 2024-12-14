"""
Advent of Code 2024, day 14
"""

import aoc_lib as aoc
from collections import defaultdict, Counter
from copy import deepcopy

lines = aoc.lines_from_file("input_14.txt")
n_rows = 103
n_cols = 101

# for testing
if False:
    n_rows = 7
    n_cols = 11
    lines = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3""".split('\n')

aoc.TablePoint.max_row = n_rows
aoc.TablePoint.max_col = n_cols

pos = []
vel = []
for line in lines:
    p_str, v_str = line.split(' v=')
    p_str = p_str[2:]
    px, py = map(int, p_str.split(','))
    vx, vy = map(int, v_str.split(','))
    # we use our TablePoint class again row = y, col = x
    pos.append(aoc.TablePoint(py, px))
    vel.append(aoc.TablePoint(vy, vx))

def print_bathroom(pos):
    c = Counter(pos)
    print()
    for row in range(n_rows):
        for col in range(n_cols):
            n = c[aoc.TablePoint(row,col)]
            if n == 0: 
                n = '.'
            elif n >= 10:
                n = '*'
            else:
                n = str(n)
            print(n, end='')
        print()
    print()

print_bathroom(pos)

end_pos = []
# 100 seconds, 100 steps
for p,v in zip(pos,vel):
    p = p + v * 100
    end_pos.append(aoc.TablePoint(p.row % n_rows, p.col % n_cols))

print_bathroom(end_pos)

ul = 0
ur = 0
ll = 0
lr = 0
for robot in end_pos:
    if robot.row <  (n_rows -1) // 2 and robot.col <  (n_cols -1) // 2 : ul += 1
    if robot.row <  (n_rows -1) // 2 and robot.col >= (n_cols +1) // 2 : ur += 1
    if robot.row >= (n_rows +1) // 2 and robot.col <  (n_cols -1) // 2 : ll += 1
    if robot.row >= (n_rows +1) // 2 and robot.col >= (n_cols +1) // 2 : lr += 1
print(ul, ur, ll, lr)

print("Answer part 1 : ", ul * ur * ll * lr)

# === Part 2

# prime numbers 101 and 103, after 101 * 103 = 10403 seconds we are back at the start position

# dunno, checked youtube, there should be none overlapping robots

for step in range(n_rows * n_cols):
    end_pos = []
    for p,v in zip(pos,vel):
        p = p + v * (step + 1)
        end_pos.append(aoc.TablePoint(p.row % n_rows, p.col % n_cols))
    s = set(end_pos)
    if len(s) == len(end_pos):
        print_bathroom(end_pos)
        break

print("Answer part 2, method 1 : ", step + 1)

# in hindsight, look for biggest blob
def find_whole_blob(tp, areas):
    areas.add(tp)
    for neighbour in tp.neighbours():
        if not neighbour in areas:
            if neighbour in end_pos:
                areas = find_whole_blob(neighbour, areas)
    return areas

max_blob = 0
steps_for_max_blob = 0

end_pos = None
for step in range(n_rows * n_cols):
    end_pos = set()
    for p,v in zip(pos,vel):
        p = p + v * (step + 1)
        end_pos.add(aoc.TablePoint(p.row % n_rows, p.col % n_cols))

    for p in end_pos:
        blob = find_whole_blob(p, set())
        if len(blob) > max_blob:
            max_blob = len(blob)
            steps_for_max_blob = step
            print(max_blob, steps_for_max_blob + 1)
            print_bathroom(end_pos)

print("Answer part 2, method 2 : ", steps_for_max_blob + 1)

