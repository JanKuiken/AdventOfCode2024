"""
Advent of Code 2024, day 2
"""

import aoc_lib as aoc

lines = aoc.lines_from_file("input_03.txt")

## for testing
#lines = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))""".split('\n')

#assert len(lines) == 1, "Oops, multiple lines"

line = '\n'.join(lines)  # undo the line splitting of aoc.lines_from_file

# i don't like regex's so i roll my own code....

def valid_mul_string(s):
    """
    Since we don't want use regex's we'll do some
    silly parsing..... just for fun...
    """
    if not s.startswith('mul('): return False
    if not s.endswith(')'): return False
    s2 = s[4:-1]
    if not ',' in s2: return False
    parts = s2.split(',')
    if len(parts) != 2: return False
    X,Y = parts
    if not valid_number(X): return False
    if not valid_number(Y): return False
    return (X,Y)

def valid_number(s):
    if len(s) < 1 or len(s) > 3: return False
    for c in s:
        if not c in '1234567890': return False
    return True    


MIN_MUL_STR_LEN = 7 # minimum length mul string 'mul(1,1)'
MAX_MUL_STR_LEN = 11 # minimum length mul string 'mul(123,123)'

line_length = len(line)
# append some silly data to the line to keep the next loop
# easier (without bounds checking)
line += "################################"
muls = []
cur = 0
while cur < line_length:
    for l in range(MIN_MUL_STR_LEN, MAX_MUL_STR_LEN+4):
        test_str = line[cur:cur+l]
        result = valid_mul_string(test_str)
        if result:
            muls.append(result)
    cur += 1
    
print(muls[:20])
part_1_result = 0
for mul in muls:
    X,Y = mul
    part_1_result += int(X) * int(Y)


print("Answer part 1 : ", end="")
print(part_1_result)

# === Part 2

muls = []
cur = 0
muls_enabled = True
while cur < line_length:
    if line[cur:cur+4] == 'do()':
        print('do()',  cur)
        muls_enabled = True
    if line[cur:cur+7] == 'don\'t()':
        print('don\'t()',  cur)
        muls_enabled = False        
    for l in range(MIN_MUL_STR_LEN, MAX_MUL_STR_LEN+4):
        test_str = line[cur:cur+l]
        result = valid_mul_string(test_str)
        if result and muls_enabled:
            muls.append(result)
    cur += 1
    
part_2_result = 0
for mul in muls:
    X,Y = mul
    part_2_result += int(X) * int(Y)

print("Answer part 2 : ", end="")
print(part_2_result)

