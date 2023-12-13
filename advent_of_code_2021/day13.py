import math
import re
import numpy as np
import copy
import itertools

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day13(array):
    point = set() #(row, col)
    i = 0
    while i < len(array):
        line = array[i]
        if line == "":
            i += 1
            break
        x, y = line.split(',')
        x = int(x)
        y = int(y)
        point.add((x, y))
        i += 1
    
    fold_instructions = []
    while i < len(array):
        line = array[i]
        instructions = line.split(" ")
        line = instructions[-1]
        axis, value = line.split('=')
        value = int(value)
        fold_instructions.append((axis, value))
        i += 1
    
    old_points = point
    is_first_fold = True
    for instruction in fold_instructions:
        axis = instruction[0]
        value = instruction[1]
        new_points = set()
        for point in old_points:
            if axis == 'x':
                if point[0] > value:
                    new_x = value - (point[0] - value)
                    new_points.add((new_x, point[1]))
                else:
                    new_points.add(point)
            else:
                if point[1] > value:
                    new_y = value - (point[1] - value)
                    new_points.add((point[0], new_y))
                else:
                    new_points.add(point)
        old_points = new_points
        if is_first_fold:
            is_first_fold = False
            print("Part 1:", len(new_points))
    
    max_x = 0
    max_y = 0
    for p in old_points:
        if p[0] > max_x:
            max_x = p[0]
        if p[1] > max_y:
            max_y = p[1]

    arr = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for p in old_points:
        x = p[0]
        y = p[1]
        arr[y][x] = "#"
    
    final_string = ""
    for r in arr:
        for c in r:
            final_string += c
        final_string += '\n'
    
    print("Part 2:")
    print(final_string.strip())

    # f = open("test.out", "w")
    # f.write(final_string)
    # f.close()
    

if __name__ == "__main__":
    filename = "input13.txt"
    arr = arrayise(filename)
    day13(arr)
    

