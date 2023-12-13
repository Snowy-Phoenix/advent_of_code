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

def get_tile(tile_map, row, col):
    if row < 0 or row >= len(tile_map):
        return 0
    if col < 0 or col >= len(tile_map[row]):
        return 0
    return tile_map[row][col]

def get_subset(steps, marked_steps):
    subset = []
    for i in range(len(marked_steps)):
        mark = marked_steps[i]
        if mark == None:
            for j in range(10):
                if i + j >= len(marked_steps):
                    break
                if marked_steps[i + j] != None:
                    break
                subset.append(steps[i + j])
            return subset
    return subset

def mark_matches(steps, marked_steps, subset, mark):
    for i in range(len(steps)):
        if marked_steps[i] == None:
            matches = True
            for j in range(len(subset)):
                if i + j >= len(steps):
                    matches = False
                    break
                if steps[i + j] != subset[j] or marked_steps[i + j] != None:
                    matches = False
                    break
            if matches:
                for j in range(len(subset)):
                    marked_steps[i + j] = mark

def find_functions(steps):
    for a in range(10, 0, -1):
        marked_steps = [None for _ in steps]

        a_subset = steps[0:a]
        mark_matches(steps, marked_steps, a_subset, "A")
        # Greedily choose the first unfilled step.
        b_subset = get_subset(steps, marked_steps)
        mark_matches(steps, marked_steps, b_subset, "B")

        c_subset = get_subset(steps, marked_steps)
        mark_matches(steps, marked_steps, c_subset, "C")
        
        is_satisfied = True
        for mark in marked_steps:
            if mark == None:
                is_satisfied = False
                break
        if is_satisfied:
            return marked_steps, a_subset, b_subset, c_subset
    return None

def day17(array):
    direction_vectors = {'n':(-1,0), 'e':(0,1), 's':(1,0), 'w':(0,-1)}
    interpreter = IntcodeInterpreter(array)
    interpreter.set_infinite_memory(True)
    scaffold_map = []

    input_stream=[]
    output_stream=[]
    interpreter.run(input_stream=input_stream, output_stream=output_stream)

    bot_row = 0
    bot_col = 0
    is_new_line = True
    for n in output_stream:
        if n == 10:
            is_new_line = True
            continue
        if n == 46:
            if is_new_line:
                scaffold_map.append([])
                is_new_line = False
            scaffold_map[-1].append(0)
        elif n == 35:
            if is_new_line:
                scaffold_map.append([])
                is_new_line = False
            scaffold_map[-1].append(1)
        elif n == 94: 
            if is_new_line:
                scaffold_map.append([])
                is_new_line = False
            scaffold_map[-1].append(1)
            bot_row = len(scaffold_map) - 1
            bot_col = len(scaffold_map[-1]) - 1
        else:
            print("Unknown Character", n)
    intersection_alignment = dict() # Coordinates, aligment parameter

    for row in range(len(scaffold_map)):
        row_map = scaffold_map[row]
        for col in range(len(row_map)):
            curr_tile = scaffold_map[row][col]
            if curr_tile == 0:
                continue
            intersections = 0
            for d in direction_vectors.values():
                new_row = row + d[0]
                new_col = col + d[1]
                new_tile = get_tile(scaffold_map, new_row, new_col)
                if new_tile == 1:
                    intersections += 1
            if intersections > 2:
                intersection_alignment[(row, col)] = row * col
    
    print("Part 1:", sum(intersection_alignment.values()))

    current_direction = 0
    directions = ['n', 'e', 's', 'w']
    steps = []
    steps_walked = 0
    while True:
        current_vector = direction_vectors[directions[current_direction]]
        new_row = bot_row + current_vector[0]
        new_col = bot_col + current_vector[1]
        next_tile = get_tile(scaffold_map, new_row, new_col)
        if next_tile == 0:
            if steps_walked > 0:
                steps.append(str(steps_walked))
            is_dead_end = True
            steps_walked = 0
            for i in (1, -1):
                next_direction = (current_direction + i) % 4
                next_vector = direction_vectors[directions[next_direction]]
                new_row = bot_row + next_vector[0]
                new_col = bot_col + next_vector[1]
                next_tile = get_tile(scaffold_map, new_row, new_col)
                if next_tile == 0:
                    continue
                else:
                    is_dead_end = False
                    current_direction = next_direction
                    if i == 1:
                        steps.append("R")
                    else:
                        steps.append("L")
            if is_dead_end:
                break
        else:
            bot_row = new_row
            bot_col = new_col
            steps_walked += 1

    main, a_subset, b_subset, c_subset = find_functions(steps)

    alen = len(a_subset)
    blen = len(b_subset)
    clen = len(c_subset)

    input_stream = []
    i = 0
    while i < len(main):
        c = main[i]
        input_stream.append(ord(c))
        input_stream.append(ord(','))
        if c == 'A':
            i += alen
        elif c == 'B':
            i += blen
        else:
            i += clen
    input_stream[-1] = 10

    for n in a_subset:
        for c in n:
            input_stream.append(ord(c))
        input_stream.append(ord(','))
    input_stream[-1] = 10

    for n in b_subset:
        for c in n:
            input_stream.append(ord(c))
        input_stream.append(ord(','))
    input_stream[-1] = 10

    for n in c_subset:
        for c in n:
            input_stream.append(ord(c))
        input_stream.append(ord(','))
    input_stream[-1] = 10
    input_stream.append(ord('n'))
    input_stream.append(10)

    print(input_stream)
    array[0] = 2
    pc = IntcodeInterpreter(array)
    pc.print_ascii_output = True
    pc.set_infinite_memory(True)
    pc.run(input_stream=input_stream)

if __name__ == "__main__":
    filename = "input17.txt"
    arr = arrayise(filename)
    arr = arr[0].split(',')
    arr = [int(i) for i in arr]
    day17(arr)