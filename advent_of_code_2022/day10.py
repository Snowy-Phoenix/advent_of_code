from collections import deque
from collections import defaultdict
import math
import os

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def solve(array):
    register = 1
    cycles = 1
    signal_strength = 0
    instruction_cycle = 0
    i = 0
    add = False
    crt = [[' ' for _ in range(40)] for _ in range(6)]
    while i < len(array):
        line = array[i]
        instruction = line.split()

        # Beginning of the cycle.
        if instruction_cycle == 0:
            if instruction[0] == 'noop':
                instruction_cycle = 1
            else:
                add = True
                instruction_cycle = 2
        
        # During
        if ((cycles + 20) % 40 == 0):
            signal_strength += cycles * register
        row = (cycles - 1) // 40 # Cycles begins at 1.
        col = (cycles - 1) % 40
        if (abs(col - register) <= 1):
            crt[row][col] = '#'
        
        # Ending
        instruction_cycle -= 1
        if (instruction_cycle == 0):
            if add:
                register += int(instruction[1])
                add = False
            i += 1
        cycles += 1
    print("Part 1:", signal_strength)
    print("Part 2:")
    for row in crt:
        for pixel in row:
            print(pixel, end='')
        print()

if __name__ == '__main__':
    filename = "input10.txt"
    arr = arrayise(filename)
    solve(arr)
