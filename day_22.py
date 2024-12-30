"""
Advent of Code 2024, day 22
"""

import aoc_lib as aoc
from collections import defaultdict, deque
from copy import deepcopy

lines = aoc.lines_from_file("input_22.txt")

# for testing
if False:
    lines = """1
10
100
2024""".split('\n')

#secret_numbers = map(int,lines)
secret_numbers = [int(i) for i in lines]

def next_secret_number(prev):
    # the definition was a bit cryptic, but this led to the example values
    next = ((prev  *   64) ^ prev) % 16777216
    next = ((next //   32) ^ next) % 16777216
    next = ((next  * 2048) ^ next) % 16777216
    return next

def two_thousandth_secret_number(secret):
    for _ in range(2000):
        secret = next_secret_number(secret)
    return secret

secret_numbers_2000 = [two_thousandth_secret_number(i) for i in secret_numbers]

print("Answer part 1 : ", sum(secret_numbers_2000))

# === Part 2

def two_thousandth_secret_number_ones_deltas(prev):
    result = []
    for _ in range(2000):
        next = next_secret_number(prev)
        result.append(next % 10 - prev % 10)
        prev = next
    return result

print(two_thousandth_secret_number_ones_deltas(123))

print("Answer part 2 : ", )
