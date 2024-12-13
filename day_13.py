"""
Advent of Code 2024, day 13
"""
import aoc_lib as aoc
from collections import defaultdict

lines = aoc.lines_from_file("input_13.txt")

# for testing
if False:
    lines = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279""".split('\n')

# parse input 
line = '\n'.join(lines)  # undo the line splitting of aoc.lines_from_file

machine_texts = line.split('\n\n')

class machine:
    def __init__(self, machine_text):
        """We trust our input, so not much checking of our input..."""
        button_a_txt, button_b_txt, prize_txt = machine_text.split('\n')
        self.button_a_x = int(button_a_txt.split(' ')[2][2:-1])
        self.button_a_y = int(button_a_txt.split(' ')[3][2:  ])
        self.button_b_x = int(button_b_txt.split(' ')[2][2:-1])
        self.button_b_y = int(button_b_txt.split(' ')[3][2:  ])
        self.prize_x    = int(prize_txt.split(' ')   [1][2:-1])
        self.prize_y    = int(prize_txt.split(' ')   [2][2:  ])

    def calculate_winable_and_tokens(self):
        """
        hmm, we need some math...

        - can we reach the prize with pushing button A `na` times and button B `nb` times
        - we have two vectors (button a & b, (x & y all positive integers (between 10 and 100?)))
        - we have one target (prize, x & y,  both big positive integers(> 1000?))
        - two equations, two unknowns (`na` & `nb)`, do we have integer solutions for `na` and `nb`?

                     na * ax + nb * bx = prizex                                           (1)
                     na * ay + nb * by = prizey                                           (2)

          (1)    =>  na = ( prizex - nb * bx) / ax                                        (3)
          (2)    =>  na = ( prizey - nb * by) / ay                                        (4)
          (3, 4) =>  ( prizex - nb * bx) / ax  = ( prizey - nb * by) / ay                 (6)
          (6)    =>  ( prizex - nb * bx) * ay  = ( prizey - nb * by) * ax                 (7)
          (7)    =>  ay * ( nb * bx - prizex ) = ax * ( nb * by - prizey)                 (8)
          (8)    =>  nb * (ay * bx) - ay * prizex = nb * (ax * by) - ax * prizey          (9)
          (9)    =>  nb * (ay * bx - ax * by)  = ay * prizex - ax * prizey                (10) 
          (10)   =>  nb = (ay * prizex - ax * prizey) / (ay * bx - ax * by)               (11)
          
          and for na something equivalent...
        """
        epsilon = 0.00001

        na =     (self.button_b_y * self.prize_x    - self.button_b_x * self.prize_y    )   \
               / (self.button_b_y * self.button_a_x - self.button_b_x * self.button_a_y )
        nb =     (self.button_a_y * self.prize_x    - self.button_a_x * self.prize_y    )   \
               / (self.button_a_y * self.button_b_x - self.button_a_x * self.button_b_y )

        self.winable =     abs(na - round(na)) < epsilon \
                       and abs(nb - round(nb)) < epsilon
        if (self.winable) :
            self.tokens = 3 * round(na) + 1 * round(nb)

machines = [machine(txt) for txt in machine_texts]

tokens_to_win_all = 0
for m in machines:
    m.calculate_winable_and_tokens()
    if m.winable:
        tokens_to_win_all += m.tokens

print("Answer part 1 : ",  tokens_to_win_all)

# === Part 2

tokens_to_win_all = 0
for m in machines: 
    m.prize_x += 10000000000000     # hmm, that's a lot...
    m.prize_y += 10000000000000
    m.calculate_winable_and_tokens()
    if m.winable:
        tokens_to_win_all += m.tokens

print("Answer part 2 : ", tokens_to_win_all)

