"""
Advent of Code 2024, day 1
"""

import aoc_lib as aoc

lines = aoc.lines_from_file("input_02.txt")

## for testing
#lines = """7 6 4 2 1
#1 2 7 8 9
#9 7 6 2 1
#1 3 2 4 5
#8 6 4 4 1
#1 3 6 7 9""".split('\n')

def sign(a):
    if a < 0: return -1
    if a > 0: return 1
    return 0

line_levels = []
line_steps = []
for line in lines:
    levels = [int(i) for i in line.split()]
    steps  = [levels[i+1]-levels[i] for i in range(len(levels)-1)]
    line_levels.append(levels)
    line_steps.append(steps)


n_save = 0
for steps in line_steps:
    save = True
    for step in steps:
        if abs(step) > 3 or sign(step) != sign(steps[0]):
            save = False
    if save:
        n_save += 1

print("Answer part 1 : ", end="")
print(n_save)

# === Part 2

# hmm, line_steps data structure used for part one are not ideal for part 2
# let's try something else....

def check_levels_org(levels):
    steps = [levels[i+1]-levels[i] for i in range(len(levels)-1)]
    for step in steps:
        if abs(step) > 3 or sign(step) != sign(steps[0]) or sign(step) == 0:
            return False
    return True

count_non_part_1 = 0
def check_levels_with_dampener(levels):
    global count_non_part_1
    if check_levels_org(levels):
        return True
    # just learned something, never have had to use this in Python
    #   https://stackoverflow.com/questions/627435/how-to-remove-an-element-from-a-list-by-index
    #   https://docs.python.org/3/tutorial/datastructures.html#the-del-statement
    count_non_part_1 += 1
    print("levels ", levels, count_non_part_1)
    for i in range(len(levels)):
        levels_copy = levels.copy()
        del levels_copy[i]
        print(levels_copy)
        if check_levels_org(levels_copy):
            return True
    return False

n_save_part_1 = 0
n_save_part_2 = 0
for levels in line_levels:
    if check_levels_org(levels):
        n_save_part_1 += 1
    if check_levels_with_dampener(levels):
        n_save_part_2 += 1

print("Answer part 1 new method : ", end="")
print(n_save_part_1)
print("Answer part 2 : ", end="")
print(n_save_part_2)


# aarrghhh
# it did not work the first time

# the missing step was adding 'or sign(step) == 0' in de conditional
# of function "check_levels_org'

# i aint gonna clean up the code
# i added some 'printf-debugging' lines and looking at those i
# wondered what to do with equal levels....

# lessons learned: - close reading...
#                  - edge cases... 

