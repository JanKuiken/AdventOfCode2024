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
                   'out' : output})

for line in initials_lines:
    wire, value = line.split(': ')
    wires[wire] = int(value)

# brute force a bit....
for _ in range(len(gates)):
    for gate in gates:
        if wires[gate['out']] == -1:
            a = wires[gate['a']] 
            b = wires[gate['b']]
            if a >= 0 and b >= 0:
                wires[gate['out']] = gate['fn'](a,b)

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

