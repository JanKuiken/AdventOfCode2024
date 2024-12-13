"""
Advent of Code 2024, day 11
"""

import aoc_lib as aoc

from collections import defaultdict

lines = aoc.lines_from_file("input_11.txt")

# for testing
#lines = """125 17""".split('\n')

stones = aoc.numbers_from_str(lines[0])

def blink(stones):
    new_stones = []
    for stone in stones:
    
        str_stone     = str(stone)
        len_str_stone = len(str_stone)
        
        if stone == 0:
            new_stones.append(1)
        elif len_str_stone % 2 == 0:
            new_stones.append(int(str_stone[:len_str_stone//2]))
            new_stones.append(int(str_stone[len_str_stone//2:]))
        else:
            new_stones.append(2024 * stone)
    return new_stones


n_blinks = 25
for i in range(n_blinks):
    stones = blink(stones)
    print(i+1, ' : ', len(stones))

print("Answer part 1 : ", len(stones))

# === Part 2

# n_blinks = 50              # fifty extra blinks, i suspect time problems.... [1]
# for i in range(n_blinks):3 
#    stones = blink(stones)
#    print(i+1, ' : ', len(stones))
#
# [1] ; yup, my computer froze for a while and after a few minutes 
#       my ipython session was killed...

# we have to think harder... or smarter...

stones = aoc.numbers_from_str(lines[0])
stones_count = defaultdict(int)
for stone in stones:
    stones_count[stone] += 1

def blink_part2(stones_count):
    new_stones_count = defaultdict(int)
    for stone, count in stones_count.items():
    
        str_stone     = str(stone)
        len_str_stone = len(str_stone)
        
        if stone == 0:
            new_stones_count[1] += count
        elif len_str_stone % 2 == 0:
            new_stones_count[int(str_stone[:len_str_stone//2])] += count
            new_stones_count[int(str_stone[len_str_stone//2:])] += count
        else:
            new_stones_count[2024 * stone] += count
    return new_stones_count

n_blinks = 75
for i in range(n_blinks):
    stones_count = blink_part2(stones_count)
    print(i+1, ' : ', sum(stones_count.values()))

print("Answer part 2 : ", sum(stones_count.values()))

