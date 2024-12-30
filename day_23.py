"""
Advent of Code 2024, day 23
"""

import aoc_lib as aoc
from collections import defaultdict, deque, Counter

lines = aoc.lines_from_file("input_23.txt")

# for testing
if False:
    lines = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn""".split('\n')
    
graph = defaultdict(list)
for line in lines:
    pc1, pc2 = line.split('-')
    graph[pc1].append(pc2)
    graph[pc2].append(pc1)

# find sets of three interconnected pc's
sets_of_three = set()
for pc1 in graph.keys():
    for pc2 in graph[pc1]:
        for pc3 in graph[pc2]:
            if pc3 in graph[pc1]:
                sets_of_three.add(tuple(sorted((pc1,pc2,pc3))))
# aoc.pprint(sets_of_three)

sets_with_pc_starting_with_a_t = set()
for pc1,pc2,pc3 in sets_of_three:
    if pc1[0] == 't' or pc2[0] == 't' or pc3[0] == 't':
        sets_with_pc_starting_with_a_t.add((pc1,pc2,pc3))
# aoc.pprint(sets_with_pc_starting_with_a_t)

print("Answer part 1 : ", len(sets_with_pc_starting_with_a_t))

# === Part 2

# can we promote a group of three to a group of four, than five,  six,....
groups_so_far = defaultdict(set)
biggest_group_so_far = 3
for threes in sets_of_three:
    groups_so_far[biggest_group_so_far].add(threes)

while True:
    for old_set in groups_so_far[biggest_group_so_far]:
        c = Counter()
        for pc in old_set:
            c.update(graph[pc])
        biggest_common_neighbour = c.most_common(1)
        # print(c, biggest_common_neighbour)
        if biggest_common_neighbour:
            neighbour_pc = biggest_common_neighbour[0][0]
            # print(neighbour_pc)
            if c[neighbour_pc] == biggest_group_so_far:
                new_set = list(old_set)
                new_set.append(neighbour_pc)
                groups_so_far[biggest_group_so_far + 1].add(tuple(sorted(new_set)))
                
    if not groups_so_far[biggest_group_so_far + 1]:
        break
    else:
        biggest_group_so_far += 1

assert len(groups_so_far[biggest_group_so_far]) == 1, "There should be one...."

print("Answer part 2 : ", ','.join(list(groups_so_far[biggest_group_so_far])[0]))

