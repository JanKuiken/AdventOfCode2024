"""
Advent of Code 2024, day 19
"""

import aoc_lib as aoc
from collections import defaultdict

lines = aoc.lines_from_file("input_19.txt")

# for testing
if False:
    lines = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb""".split('\n')

towels = lines[0].split(', ')
designs = lines[2:]

# brute force with combinations and permutations did not work... too slow...

# if we don't have duplicates were gonna use a set instead of a list for the towels
assert len(set(towels)) == len(towels), "Oops we have duplicates in towels"
towels = set(towels)

lengths = list(map(len, towels))
max_towel_len  = max(lengths)
min_towel_len  = min(lengths)

def splits(s):
    n = len(s)
    max_head_len = min(max_towel_len, n)
    for i in range(1,max_head_len+1):
        yield s[:i], s[i:]

# recurisve function to check if a (tailing part of a) design can be matched
cannot_be_matched = set()
def can_be_matched(s):
    global cannot_be_matched
    if s in cannot_be_matched:
        return False
    if s in towels or s=='':
        return True
    matched = False
    for head, tail in splits(s):
        if head in towels and can_be_matched(tail):
            matched = True
            break
    if not matched:
        cannot_be_matched.add(s)
    return matched

count = 0
for design in designs:
    if can_be_matched(design):
        count += 1

print("Answer part 1 : ", count)

# === Part 2

print("Answer part 2 : ", )

