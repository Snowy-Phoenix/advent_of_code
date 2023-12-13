import math
import re
import numpy as np
import itertools
from intcode import IntcodeInterpreter
import copy

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day19a(array):
    interpreter = IntcodeInterpreter(array)
    interpreter.set_infinite_memory(True)

    tractor_beam = []
    hits = 0
    for i in range(50):
        tractor_beam.append([])
        for j in range(50):
            input_stream = [j, i]
            output_stream = []
            interpreter.run(input_stream=input_stream, output_stream=output_stream)
            if output_stream[0]:
                hits += output_stream[0]
                tractor_beam[-1].append('#')
            else:
                tractor_beam[-1].append('.')
    print("Part 1:", hits)
    
    
def find_y(interpreter, start_x, start_y, direction=1):
    y = start_y
    while True:
        input_stream = [start_x, y]
        output_stream = []
        interpreter.run(input_stream=input_stream, output_stream=output_stream)
        if output_stream[0] == 1:
            break
        else:
            y += direction
        if abs(y) > 10000:
            print(y)
            raise Exception
    return y

def can_fit_top_right(interpreter, x, y, size):
    can_fit = True
    for i in range(size):
        input_stream = [x - i, y + i]
        output_stream = []
        interpreter.run(input_stream=input_stream, output_stream=output_stream)
        if output_stream[0] == 0:
            can_fit = False
            break
    return can_fit

def day19b(array):
    interpreter = IntcodeInterpreter(array)
    interpreter.set_infinite_memory(True)
    low_x = 8
    low_y = 0
    while True:
        input_stream = [low_x, low_y]
        output_stream = []
        interpreter.run(input_stream=input_stream, output_stream=output_stream)
        if output_stream[0] == 1:
            break
        else:
            low_y += 1
    # Find the upper bound of x.
    high_x = low_x
    high_y = low_y
    while True:
        high_x = low_x * 2
        # Find high_y at high_x
        high_y = find_y(interpreter, high_x, low_y, 1)
        # Verify that we can fit a 100x100 box.
        can_fit = can_fit_top_right(interpreter, high_x, high_y, 100)
        if can_fit:
            break
        else:
            low_x = high_x
            low_y = high_y
    # Use binary search to find where the 100x100 box fits.
    while low_x < high_x:
        mid_x = (high_x + low_x) // 2
        mid_y = find_y(interpreter, mid_x, low_y)
        can_fit = can_fit_top_right(interpreter, mid_x, mid_y, 100)
        if can_fit:
            high_x = mid_x
            high_y = find_y(interpreter, high_x, high_y, -1)
        else:
            low_x = mid_x + 1
            low_y = find_y(interpreter, low_x, low_y, 1)
    
    # Find the ranges of x values that could contain the box.
    lower_range = low_x - (low_x // 100)
    upper_range = high_x + (high_x // 100)
    y = find_y(interpreter, lower_range, 0)
    for i in range(lower_range, upper_range, 1):
        curr_y = find_y(interpreter, i, y)
        if can_fit_top_right(interpreter, i, curr_y, 100):
            print("Part 2:", ((i - 99) * 10000) + curr_y)
            return
    
    
if __name__ == "__main__":
    filename = "input19.txt"
    arr = arrayise(filename)
    arr = arr[0].split(',')
    arr = [int(i) for i in arr]
    day19a(arr)
    day19b(arr)