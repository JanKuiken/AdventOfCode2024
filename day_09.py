"""
Advent of Code 2024, day 9
"""

import aoc_lib as aoc

#from collections import defaultdict
#from itertools import combinations, permutations
from collections import namedtuple


lines = aoc.lines_from_file("input_09.txt")

# for testing
DEBUG = False
if DEBUG: lines = """2333133121414131402""".split('\n')

line = lines[0]

# disk is represented by a list of integer
# for part 2 we add a 'Chunk'
Chunk = namedtuple("Chunk", "file_number disk_index length")

def fill_disk():
    disk = []
    chunks = []
    disk_index = 0 # for part 2
    for pos, length in enumerate([int(i) for i in line]):
        if pos % 2 == 0:
            file_number = pos // 2
        else:
            file_number = -1  # -1 is representing empty space
        chunks.append(Chunk(file_number, disk_index, length))
        for i in range(length):
            disk.append(file_number)
            disk_index += 1
        
    return disk, chunks

# only useful for the test data
def print_disk(disk): 
    for i, file_number in enumerate(disk):
        if file_number == -1 : print('.', end='')
        else : print(file_number, end='')
    print()

empty_index = None
full_index = None

def defrag_part_1():
    global disk, empty_index, full_index
    empty_index = 0
    full_index = len(disk) -1
    def set_next_empty_index():
        global empty_index
        while (empty_index < len(disk) and disk[empty_index] != -1):
            empty_index += 1

    def set_prev_full_index():
        global full_index
        while (full_index >= 0 and disk[full_index] == -1):
            full_index -= 1

    # defrag
    set_next_empty_index()
    set_prev_full_index()
    while empty_index < full_index:
        disk[empty_index], disk[full_index] = disk[full_index], disk[empty_index]  
        set_next_empty_index()
        set_prev_full_index()
        if DEBUG: print_disk(disk)


# calculate checksum
def calc_checksum():
    checksum = 0
    for i,filenumber in enumerate(disk):
        if filenumber != -1:
            checksum += i * filenumber
    return checksum

disk, dummy = fill_disk()
if DEBUG: print_disk(disk)
defrag_part_1()
checksum = calc_checksum()

print("Answer part 1 : ", checksum)

# === Part 2

def defrag_part_2():
    global disk
    if DEBUG: print_disk(disk)
    file_chunks = []
    for chunk in chunks:
        if chunk.file_number != -1:
            file_chunks.append(chunk)
    file_chunks.reverse()
    for chunk in file_chunks:
        # find chunk.length free blocks on the disk
        suitable_start_index = None
        for start_disk_index, block in enumerate(disk):
            if block == -1:
                free_length = 1
                while start_disk_index + free_length < len(disk) and disk[start_disk_index + free_length] == -1:
                    free_length += 1
                if free_length >= chunk.length:
                    suitable_start_index = start_disk_index
                    break   # from `for start_disk_index...` loop 
        if suitable_start_index and suitable_start_index < chunk.disk_index:
            # move file
            for i in range(chunk.length):
                disk[suitable_start_index + i] = chunk.file_number
                disk[chunk.disk_index + i] = -1
            if DEBUG: print_disk(disk)

disk, chunks = fill_disk()
if DEBUG: print(chunks)
defrag_part_2()
checksum = calc_checksum()


print("Answer part 2 : ", checksum)

