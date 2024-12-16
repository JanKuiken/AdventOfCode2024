"""
Advent of Code 2024, day 15
"""

import aoc_lib as aoc
from collections import defaultdict
from copy import deepcopy

lines = aoc.lines_from_file("input_15.txt")
lines = '\n'.join(lines)

# for testing
if False:
    lines = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

# personal test case
if False:         
    lines = """#######
#...#.#
#.....#
#.OOO.#
#.@O..#
#.....#
#######

^v>>v>>^"""




house, moves = lines.split('\n\n')
house = house.split('\n')
moves = moves.replace('\n', '')
matrix = [ [ c for c in line ] for line in house ]

n_rows = len(matrix)
n_cols = len(matrix[0])

LEFT  = aoc.TablePoint(0,-1)
RIGHT = aoc.TablePoint(0,+1)
UP    = aoc.TablePoint(-1,0)
DOWN  = aoc.TablePoint(+1,0)

directions = { '<' : LEFT  ,
               '>' : RIGHT ,
               '^' : UP    ,
               'v' : DOWN   }
current_pos = None
for row in range(n_rows):
    for col in range(n_cols):
        if matrix[row][col] == '@':
            current_pos =aoc.TablePoint(row,col)

for move in moves:
    target = current_pos + directions[move]
    if matrix[target.row][target.col] == '#':
        pass
    elif matrix[target.row][target.col] == '.':
        matrix[target.row][target.col] = '@'
        matrix[current_pos.row][current_pos.col] = '.'
        current_pos = target
    elif matrix[target.row][target.col] == 'O':
        for n in range(1, max([n_rows, n_cols])):
            next = current_pos + directions[move] * n
            if matrix[next.row][next.col] == '#':
                break
            elif matrix[next.row][next.col] == '.':
                matrix[target.row][target.col] = '@'
                matrix[current_pos.row][current_pos.col] = '.'
                matrix[next.row][next.col] = 'O'
                current_pos = target
                break
             
aoc.print_matrix(matrix)
sum_gps_coor = 0
for row in range(n_rows):
    for col in range(n_cols):
        if matrix[row][col] == 'O':
            sum_gps_coor += 100 * row + col

print("Answer part 1 : ", sum_gps_coor)

# === Part 2

# this is a bit more complicated, we probably need some functions to keep
# things clear... 
# ... and it might be useful to store the boxes in another way than cells
#     in the matrix....

matrix = []
for line in house:
    row = []
    for c in line:
        if c == '#':
            row.append('#')
            row.append('#')
        if c == '.':
            row.append('.')
            row.append('.')
        if c == 'O':
            row.append('[')
            row.append(']')
        if c == '@':
            row.append('@')
            row.append('.')
    matrix.append(row)

aoc.print_matrix(matrix)

n_rows = len(matrix)
n_cols = len(matrix[0])

current_pos = None
for row in range(n_rows):
    for col in range(n_cols):
        if matrix[row][col] == '@':
            current_pos =aoc.TablePoint(row,col)



# boxes are stored in a defaultdict(bool), the bool will be used as a move flag...
boxes = defaultdict(bool)

for row in range(n_rows):
    for col in range(n_cols):
        if matrix[row][col] == '[':
            boxes[aoc.TablePoint(row,col)]
            matrix[row][col] = '.'
        if matrix[row][col] == ']':
            matrix[row][col] = '.'

aoc.print_matrix(matrix)

def reset_boxes_bools():
    global boxes
    for box in boxes.keys():
        boxes[box] = False

def move_boxes(direction):
    global boxes
    temp_boxes = defaultdict(bool)
    for box, move_flag in boxes.items():
        if move_flag:
            temp_boxes[box + direction] = False
        else:
            temp_boxes[box] = False
    boxes = deepcopy(temp_boxes)


def get_box_at_pos(pos):
    if pos in boxes.keys(): return pos
    left = pos + LEFT
    if left in boxes.keys(): return left
    return None

def can_box_at_pos_move(pos, direction):
    box = get_box_at_pos(pos)
    assert box, "Oops, no box at pos"
    if direction in [LEFT, RIGHT]:
        return can_box_move_horizontal(box, direction)
    if direction in [UP, DOWN]:
        return can_box_move_vertical(box, direction)
    assert box, "Oops, unknown direction"

def can_box_move_horizontal(box, direction):
    global boxes
    
    if direction == RIGHT:
        check_pos =  box + RIGHT * 2
    else:
        check_pos =  box + LEFT

    check_box = get_box_at_pos(check_pos)

    if matrix[check_pos.row][check_pos.col] == '#':
        boxes[box] = False
        return False

    if check_box:
        result = can_box_move_horizontal(check_box, direction)
        boxes[box] = result
        return result

    boxes[box] = True 
    return True

    
def can_box_move_vertical(box, direction):
    # print('can_box_move_vertical called with box : ', box)
    global boxes
    
    if direction == UP:
        check_pos_1 =  box + UP
        check_pos_2 =  box + RIGHT + UP
    else:
        check_pos_1 =  box + DOWN
        check_pos_2 =  box + RIGHT + DOWN

    check_box_1 = get_box_at_pos(check_pos_1)
    check_box_2 = get_box_at_pos(check_pos_2)

    check_pos_1_type = None
    if matrix[check_pos_1.row][check_pos_1.col] == '#':
        check_pos_1_type = '#'
    elif get_box_at_pos(check_pos_1):
        box_1 = get_box_at_pos(check_pos_1)
        if can_box_move_vertical(box_1, direction):
            check_pos_1_type = 'B'  # box that can be moved
        else:
            check_pos_1_type = 'b'  # box that can NOT be moved
    else:
        check_pos_1_type = '.'

    # repeat for pos_2
    check_pos_2_type = None
    if matrix[check_pos_2.row][check_pos_2.col] == '#':
        check_pos_2_type = '#'
    elif get_box_at_pos(check_pos_2):
        box_2 = get_box_at_pos(check_pos_2)
        if can_box_move_vertical(box_2, direction):
            check_pos_2_type = 'B'  # box that can be moved
        else:
            check_pos_2_type = 'b'  # box that can NOT be moved
    else:
        check_pos_2_type = '.'

    # print('check_pos_x_types : ', check_pos_1_type, ' ', check_pos_2_type)
    
    if  (    (check_pos_1_type ==  '.' and check_pos_2_type == '.')
          or (check_pos_1_type ==  '.' and check_pos_2_type == 'B')
          or (check_pos_1_type ==  'B' and check_pos_2_type == '.')
          or (check_pos_1_type ==  'B' and check_pos_2_type == 'B') ) :

        boxes[box] = True
        return True
    else:
        return False

def bah_print_matrix():
    # bah debugging
    bah = deepcopy(matrix)
    for box in boxes.keys():
        bah[box.row][box.col] = '['
        other = box + RIGHT
        bah[other.row][other.col] = ']'
    aoc.print_matrix(bah)

# oke, the main stuff again...
for move in moves:

    reset_boxes_bools()
    target = current_pos + directions[move]
    target_box = get_box_at_pos(target)
    
    #bah_print_matrix()
    #print(move, current_pos, target, target_box)

    if matrix[target.row][target.col] == '#':
        pass
    elif target_box:
        #print(boxes)
        if can_box_at_pos_move(target_box, directions[move]):
            #print(boxes)
            move_boxes(directions[move])            
            matrix[current_pos.row][current_pos.col] = '.'
            matrix[target.row][target.col] = '@'
            current_pos = target
    else:
        matrix[current_pos.row][current_pos.col] = '.'
        matrix[target.row][target.col] = '@'
        current_pos = target

#bah_print_matrix()

# add boxes symbols back to the matrix
for box in boxes.keys():
    matrix[box.row][box.col] = '['
    other = box + RIGHT
    matrix[other.row][other.col] = ']'
    
aoc.print_matrix(matrix)

sum_gps_coor = 0
for row in range(n_rows):
    for col in range(n_cols):
        if matrix[row][col] == '[':
            sum_gps_coor += 100 * row + col

print("Answer part 2 : ", sum_gps_coor)


