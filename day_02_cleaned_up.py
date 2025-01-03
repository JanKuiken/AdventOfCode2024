"""
Advent of Code 2024, day 2
"""

import aoc_lib as aoc

lines = aoc.lines_from_file("input_02.txt")

line_levels = []
for line in lines:
    levels = [int(i) for i in line.split()]
    line_levels.append(levels)

def check_levels_part_1(levels):
    steps = [levels[i+1]-levels[i] for i in range(len(levels)-1)]
    for step in steps:
        if    abs(step) > 3                          \
           or aoc.sign(step) != aoc.sign(steps[0])   \
           or aoc.sign(step) == 0:
            return False
    return True

def check_levels_part_2(levels):
    if check_levels_part_1(levels):
        return True
    for i in range(len(levels)):
        levels_copy = levels.copy()
        del levels_copy[i]
        if check_levels_part_1(levels_copy):
            return True
    return False

n_save_part_1 = 0
n_save_part_2 = 0
for levels in line_levels:
    if check_levels_part_1(levels):
        n_save_part_1 += 1
    if check_levels_part_2(levels):
        n_save_part_2 += 1

print("Answer part 1 : ", n_save_part_1)
print("Answer part 2 : ", n_save_part_2)

