"""
Advent of Code 2024, day 1
"""

import aoc_lib as aoc

lines = aoc.lines_from_file("input_01.txt")

list_1 = []
list_2 = []
for line in lines:
    part_1, part_2 = line.split()
    list_1.append(int(part_1))
    list_2.append(int(part_2))

list_1.sort()
list_2.sort()

total = 0
for id_1, id_2 in zip(list_1, list_2):
    total += abs(id_1 - id_2)

print("Answer part 1 : ", end="")
print(total)


# === Part 2

total = 0

for id_1 in list_1:
    times = 0
    for id_2 in list_2:
        if id_1 == id_2:
            times += 1
    total += id_1 * times

print("Answer part 2 : ", end="")
print(total)

