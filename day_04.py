"""
Advent of Code 2024, day 4
"""

import aoc_lib as aoc

table = aoc.lines_from_file("input_04.txt")

## for testing
#table = """MMMSXXMASM
#MSAMXMSMSA
#AMXSXMAAMM
#MSAMASMSMX
#XMASAMXAMM
#XXAMMXXAMA
#SMSMSASXSS
#SAXAMASAAA
#MAMMMXMMMM
#MXMXAXMASX""".split('\n')

width = len(table[0])
height = len(table)

# i added a small but nifty TablePoint class to my aoc_lib.py....

aoc.TablePoint.max_col = width
aoc.TablePoint.max_row = height

directions = [ aoc.TablePoint(-1,  0), 
               aoc.TablePoint(-1,  1),
               aoc.TablePoint( 0,  1),
               aoc.TablePoint( 1,  1),
               aoc.TablePoint( 1,  0),
               aoc.TablePoint( 1, -1),
               aoc.TablePoint( 0, -1),
               aoc.TablePoint(-1, -1), ]

n_xmas = 0
for row in range(height):
    for col in range(width):
        cell_1 = aoc.TablePoint(row, col)
        for dir in directions: # (i don't care nothing about overwriting Python's dir function in this case....)
            cell_2 = cell_1 + dir * 1
            cell_3 = cell_1 + dir * 2
            cell_4 = cell_1 + dir * 3
            if cell_4.isInbounds():
                if     table[cell_1.row][cell_1.col] == 'X' \
                   and table[cell_2.row][cell_2.col] == 'M' \
                   and table[cell_3.row][cell_3.col] == 'A' \
                   and table[cell_4.row][cell_4.col] == 'S' : n_xmas += 1 


print("Answer part 1 : ", end="")
print(n_xmas)

# === Part 2

n_xmas = 0
for row in range(height):
    for col in range(width):
        centre = aoc.TablePoint(row, col)
        if table[centre.row][centre.col] == 'A':
            ul = centre + aoc.TablePoint(-1,-1)   # uppler-left to lower-right...
            ur = centre + aoc.TablePoint(-1,+1)
            ll = centre + aoc.TablePoint(+1,-1)
            lr = centre + aoc.TablePoint(+1,+1)
            if      ul.isInbounds() \
                and ur.isInbounds() \
                and ll.isInbounds() \
                and lr.isInbounds() :
                   ul = table[ul.row][ul.col]  # i don't care ul changes from type TablePoint to char
                   ur = table[ur.row][ur.col]
                   lr = table[lr.row][lr.col]
                   ll = table[ll.row][ll.col]
                   ul_oke = (ul == 'M' and lr == 'S') or (ul == 'S' and lr == 'M') 
                   ur_oke = (ur == 'M' and ll == 'S') or (ur == 'S' and ll == 'M') 
                   if ul_oke and ur_oke:
                       n_xmas += 1


print("Answer part 2 : ", end="")
print(n_xmas)

