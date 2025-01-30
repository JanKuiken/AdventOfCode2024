"""
Advent of Code 2024, day 5
"""

import aoc_lib as aoc
from collections import defaultdict
from functools import cmp_to_key

lines = aoc.lines_from_file("input_05.txt")

# for testing
# lines = aoc.lines_from_file("input_05_test.txt")

# store the data in useful structures...
rule_lines, update_lines = '\n'.join(lines).split('\n\n')
rules = defaultdict(list)     # rules are stored default dict with empty list as default
updates = []                  # updates are stored in a list of lists

rules_part = True
for line in lines:
    if line == '':        
        rules_part = False
    else:
        if rules_part: 
            k,v =line.split('|')
            rules[int(k)].append(int(v))
        else:
            updates.append([int(i) for i in line.split(',')])

# check if updates are valid
valid_updates = []
invalid_updates = [] # added for part 2
for update in updates:
    update_is_valid = True
    printed_pages = []
    for page in update:
        if page in rules.keys():
            for later_page in rules[page]:
                if later_page in printed_pages:
                    update_is_valid = False
        printed_pages.append(page)
    if update_is_valid:
        valid_updates.append(update)
    else:
        invalid_updates.append(update)

def sum_of_middle_page_numbers(updates):
    sum = 0
    for update in updates:
        # check if the numbers of pages are odd
        assert len(update) % 2 == 1, 'Oops even number of pages in valid update'
        sum += update[len(update) // 2]
    return sum

print("Answer part 1 : ", sum_of_middle_page_numbers(valid_updates))

# === Part 2

# oke, we need to change the order of the invalid_updates....

# aargh, i don.t know how....

# 1) rebuild updates and insert pages at correct place? ... hmm difficult
# 2) sort with handbuilt bubble sort? ... can go wrong in a thousend ways..
# 3) using Python sort with a cunning key function...
#      google,google:
#          need to: from functools import cmp_to_key
#                   write a cunning compare function (trial and error...)

def comapare_pages(page_a, page_b):
    if page_a in rules.keys():
        if page_b in rules[page_a]:
            return -1
    return 1

corrected_invalid_updates = [ sorted(update, key=cmp_to_key(comapare_pages)) for update in invalid_updates ]

print("Answer part 2 : ", sum_of_middle_page_numbers(corrected_invalid_updates))

