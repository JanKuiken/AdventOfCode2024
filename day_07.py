"""
Advent of Code 2024, day 7
"""

import aoc_lib as aoc
from itertools import product

lines = aoc.lines_from_file("input_07.txt")

# for testing
#lines = """190: 10 19
#3267: 81 40 27
#83: 17 5
#156: 15 6
#7290: 6 8 6 15
#161011: 16 10 13
#192: 17 8 14
#21037: 9 7 18 13
#292: 11 6 16 20""".split('\n')

result = 0

for line in lines:
    answer, operand_list = line.split(': ')
    answer = int(answer)
    operands = [int(i) for i in operand_list.split()]
    can_be_done = False
    for operators in product('+*', repeat=len(operands)-1):
        temp = operands[0]
        for operator, number in zip(operators, operands[1:]):
            if operator == '+':
                temp += number
            else:
                temp *= number
        if temp == answer:
            can_be_done = True
    if can_be_done:
        result += answer

print("Answer part 1 : ", result)


# === Part 2

result = 0

for line in lines:
    answer, operand_list = line.split(': ')
    answer = int(answer)
    operands = [int(i) for i in operand_list.split()]
    can_be_done = False
    for operators in product('+*|', repeat=len(operands)-1):
        temp = operands[0]
        for operator, number in zip(operators, operands[1:]):
            if operator == '+':
                temp += number
            elif operator == '*':
                temp *= number
            else:
                temp = int(str(temp) + str(number))
        if temp == answer:
            can_be_done = True
    if can_be_done:
        result += answer

print("Answer part 2 : ", result)

