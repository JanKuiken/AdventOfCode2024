"""
Advent of Code 2024, day 24
"""

import aoc_lib as aoc
from collections import defaultdict, deque, Counter

lines = aoc.lines_from_file("input_24.txt")

# for testing
if False:
    lines = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj""".split('\n')

lines = '\n'.join(lines)
    
initial_lines, connection_lines = lines.split('\n\n')
initials_lines   = initial_lines.split('\n')
connection_lines = connection_lines.split('\n')

# we use -1 as unknown, these are our operators
def XOR(a,b):
    if (a==1 and b==0) or (a==0 and b==1): return 1
    if (a==1 and b==1) or (a==0 and b==0): return 0
    return -1

def AND(a,b):
    if (a==1 and b==1): return 1
    if (a==0 and b==0) or (a==0 and b==1) or (a==1 and b==0): return 0
    return -1

def OR(a,b):
    if (a==0 and b==1) or (a==1 and b==0) or (a==1 and b==1): return 1
    if (a==0 and b==0): return 0
    return -1

# parse the input
gates = []
wires = {}
for line in connection_lines:
    begin, output  = line.split(' -> ')
    a, operator ,b = begin.split(' ')
    fn = OR
    if operator == 'AND': fn = AND
    if operator == 'XOR': fn = XOR
    wires[a] = -1
    wires[b] = -1
    wires[output] = -1
    gates.append({ 'a'   : a,
                   'b'   : b,
                   'fn'  : fn,
                   'out' : output })

for line in initials_lines:
    wire, value = line.split(': ')
    wires[wire] = int(value)

# brute force a bit....
def solve():
    global wires
    for _ in range(len(gates)):
        for gate in gates:
            if wires[gate['out']] == -1:
                a = wires[gate['a']] 
                b = wires[gate['b']]
                if a >= 0 and b >= 0:
                    wires[gate['out']] = gate['fn'](a,b)
solve()

def get_xyz_value(xy_or_z_str):
    output = ''
    keys = list(wires.keys())
    keys.sort(reverse=True)
    for key in keys:
        if key.startswith(xy_or_z_str):
            output += str(wires[key])
    return int(output, base=2)

print("Answer part 1 : ", get_xyz_value('z'))

# === Part 2

print("Answer part 2 : ", )

# hmm,... can this be brute forced...
# or do we have to figure out the circuit and fix it to a correct adder...
# we have ca. 200 outputs, 200^8 is too much, so no brute force...
# - do we also have to change the inputs x and y? not clear from the description
# - some background....
#    https://en.wikipedia.org/wiki/Adder_(electronics)#/media/File:Fulladder.gif
#    https://en.wikipedia.org/wiki/Adder_(electronics)
# - can we find this adder circuit in our circuit....

count = 0
for gate in gates:
    if (     gate['fn'] == AND
         and (    (gate['a'].startswith('x') and gate['b'].startswith('y')) 
               or (gate['a'].startswith('y') and gate['b'].startswith('x')) )) :
        print(gate)
        count += 1
print(count)

count = 0
for gate in gates:
    if (     gate['fn'] == XOR
         and (    (gate['a'].startswith('x') and gate['b'].startswith('y')) 
               or (gate['a'].startswith('y') and gate['b'].startswith('x')) )) :
        print(gate)
        count += 1
print(count)

count = 0
for gate in gates:
    if gate['fn'] == XOR and gate['out'].startswith('z'):
        print(gate)
        count += 1
print(count)

count = 0
keys = list(wires.keys())
keys.sort(reverse=True)
for key in keys:
    if key.startswith('z'):
        count += 1
print(count)

print('Evaluate and think moment....\n\n')

# check, the real problem behaves better than the example problem...
#  - all x's are connected to an XOR with the corresponding y's
#  - all x's are connected to an AND with the corresponding y's
# this looks like an adder circuit....
# 90 of the 222 gates accounted for
# 90 + 3x45 = 225, maybe the gates for the last carry bit are missing

# - not all z's are outputted from an XOR
# - z45 is output from an OR, the last carry?

# Oops, nerd joke ahead....
# "carry on"   # (https://en.wikipedia.org/wiki/Keep_Calm_and_Carry_On)

post_fixes = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
              '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
              '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
              '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
              '40', '41', '42', '43', '44' ]

# create dicts with gate no's of the 'primary' XOR's and AND's
first_xors = defaultdict(str)
first_ands = defaultdict(str)
for pf in post_fixes:    
    input = 'x' + pf
    for i, gate in enumerate(gates):
        if  gate['fn'] == XOR and (gate['a'] == input or gate['b'] == input):
            first_xors[pf] = i
        if  gate['fn'] == AND and (gate['a'] == input or gate['b'] == input):
            first_ands[pf] = i

print('len(first_xors)', len(first_xors))
print('first_xors', first_xors)
print('len(first_ands)', len(first_ands))
print('first_ands', first_ands)

# create dicts with gate no's of the 'secondary' XOR's and AND's
# these have inputs connected to the primaries XOR's ouputs
second_xors = defaultdict(str)
second_ands = defaultdict(str)
for pf in post_fixes:
    primary_xor_gate = first_xors[pf]
    input = gates[primary_xor_gate]['out']
    for i, gate in enumerate(gates):
        if  gate['fn'] == XOR and (gate['a'] == input or gate['b'] == input):
            second_xors[pf] = i
        if  gate['fn'] == AND and (gate['a'] == input or gate['b'] == input):
            second_ands[pf] = i

print('len(second_xors)', len(second_xors))
print('second_xors', second_xors)
print('len(second_ands)', len(second_ands))
print('second_ands', second_ands)

third_ors = defaultdict(str)
for pf in post_fixes:
    primary_and_gate = first_ands[pf]
    secondary_and_gate = second_ands[pf]
    if isinstance(primary_and_gate, int) and isinstance(secondary_and_gate, int):
        input_1 = gates[primary_and_gate]['out']   if gates[primary_and_gate] else ''
        input_2 = gates[secondary_and_gate]['out'] if gates[secondary_and_gate] else ''
        for i, gate in enumerate(gates):
            if  gate['fn'] == OR and (    (gate['a'] == input_1 and gate['b'] == input_2)
                                       or (gate['a'] == input_2 and gate['b'] == input_1) ) :
                third_ors[pf] = i

print('len(third_ors)', len(third_ors))
print('third_ors', third_ors)

# hmm we miss two secondary XOR's
# first for x00,y00 and z00 might be correct, there is no carry-in for 00
#  (first missing gate explained, two to go....)
# the 'top' AND for the 00's can also be missing
# the 'bottom' AND for z45 can also be missing
# so that are the three missing gates

# now find the errors in the circuit and find the output swaps to correct them...
# lets do some ASCII art to 'draw' the circuit roughly like the wikipedia picture

matrix = [ [' ' for i in range(100) ]for _ in range(45*7) ]
def matrix_print(s, row, col):
    print(s, row,col)
    for i,c in enumerate(s):
        matrix[row][col+i] = c

not_printed = list(range(len(gates)))
for stuff in [ (first_xors,   0, 1),
               (first_ands,   3, 1),
               (second_xors,  0, 21),
               (second_ands,  3, 21),
               (third_ors,    3, 41), ]:
    for i, pf in enumerate(post_fixes):
        row = i * 7 + stuff[1]
        col = stuff[2]
        if isinstance(stuff[0][pf], int):
            not_printed.remove(stuff[0][pf])
            gate = gates[stuff[0][pf]]
            if gate:
                #print('gate', gate, row, col)
                G = ' OR'
                if gate['fn'] == XOR: G = 'XOR'
                if gate['fn'] == AND: G = 'AND'
                matrix_print(gate['a']  , row  , col   )
                matrix_print(gate['b']  , row+1, col   )
                matrix_print(G          , row+1, col+4 )
                matrix_print(gate['out'], row+1, col+10)

aoc.print_matrix(matrix)
for i in not_printed:
    print(gates[i])

