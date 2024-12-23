"""
Advent of Code 2024, day 18
"""

import aoc_lib as aoc
from collections import defaultdict, deque

lines = aoc.lines_from_file("input_18.txt")
size = 71
part_1_bytes = 1024

# for testing
if False:
    size = 7
    part_1_bytes = 12
    lines = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0""".split('\n')

aoc.TablePoint.max_row = size
aoc.TablePoint.max_col = size

matrix = [ [ '.' for _ in range(size) ] for _ in range(size) ]
for line in lines[:part_1_bytes]:
    col, row = map(int, line.split(','))
    matrix[row][col] = '#'
aoc.print_matrix(matrix)

#create a graph
graph = defaultdict(set)
for row in range(size):
    for col in range(size):
        if matrix[row][col] == '.':
            tp1 = aoc.TablePoint(row,col)
            for tp2 in tp1.cartesian_neighbours():
                if matrix[tp2.row][tp2.col] == '.':
                    graph[tp1].add(tp2)
                    graph[tp2].add(tp1)

A_LOT = 9999999999
depth = [ [ A_LOT for _ in range(size) ] for _ in range(size) ]

def bfs(start):  # see https://en.wikipedia.org/wiki/Breadth-first_search
    Q = deque()
    seen = set()
    Q.append(start)
    seen.add(start)
    depth[start.row][start.col] = 0
    while Q:
        v = Q.popleft()
        for w in graph[v]:
            if not w in seen:
                depth[w.row][w.col] = depth[v.row][v.col] + 1
                Q.append(w)        
                seen.add(w)
                if w == aoc.TablePoint(size-1, size-1):
                    return
                
bfs(aoc.TablePoint(0,0))

print("Answer part 1 : ", depth[size-1][size-1])

# === Part 2

tp = None
for line in lines[part_1_bytes:]:
    col, row = map(int, line.split(','))
    tp = aoc.TablePoint(row,col)
    if tp in graph.keys():
        del graph[tp]  # deleteing this item will do the trick
    depth = [ [ A_LOT for _ in range(size) ] for _ in range(size) ]
    bfs(aoc.TablePoint(0,0))
    if depth[size-1][size-1] == A_LOT:
        break        

print("Answer part 2 : ", ','.join(map(str,[tp.col, tp.row])))

