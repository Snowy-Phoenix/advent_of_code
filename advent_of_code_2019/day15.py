import math
import re
import numpy as np
import itertools
from intcode import IntcodeInterpreter

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def print_map(tile_map, curr_row, curr_col):
    full_map = ""
    for row in range(len(tile_map)):
        for col in range(len(tile_map[row])):
            if row == curr_row and col == curr_col:
                full_map += "X"
            else:
                full_map += tile_map[row][col]
        full_map += "\n"
    print(full_map)

def day15_manual(interpreter):
    tile_map = [[" " for _ in range(41)] for _ in range(41)]
    curr_row = 21
    curr_col = 21
    input_directions = {"w":(-1,0), "d":(0,1), "s":(1,0), "a":(0,-1)}
    reversed_directions = {(1,0):(-1,0), (0,-1):(0,1), (-1,0):(1,0), (0,1):(0,-1)}

    input_stream = []

    while True:
        direction = input().lower()
        if direction == 'w':
            input_stream = [1]
        elif direction == 'd':
            input_stream = [4]
        elif direction == 's':
            input_stream = [2]
        elif direction == 'a':
            input_stream = [3]
        else:
            direction = 'w'
            input_stream = [1]

        direction_vector = input_directions[direction]
        
        output_stream = []
        interpreter.run(input_stream=input_stream, output_stream=output_stream)
        if interpreter.halted:
            break

        new_row = curr_row + direction_vector[0]
        new_col = curr_col + direction_vector[1]
        if output_stream[0] == 0:
            tile_map[new_row][new_col] = '#'
        elif output_stream[0] == 1:
            tile_map[new_row][new_col] = '.'
            curr_row = new_row
            curr_col = new_col
        elif output_stream[0] == 2:
            tile_map[new_row][new_col] = 'O'
            curr_row = new_row
            curr_col = new_col

        print_map(tile_map, curr_row, curr_col)

def get_time_for_oxy_to_fill(tile_map, start_row, start_col):
    directions = {(-1,0), (0,1), (1,0), (0,-1)}
    queue = [(start_row, start_col)]
    new_coords = []
    minutes = 0
    while True:
        if len(queue) == 0:
            return minutes - 1
        for coords in queue:
            row = coords[0]
            col = coords[1]
            for d in directions:
                new_row = row + d[0]
                new_col = col + d[1]
                if tile_map[new_row][new_col] == '.':
                    tile_map[new_row][new_col] = 'O'
                    new_coords.append((new_row, new_col))
        queue = new_coords
        new_coords = []
        minutes += 1
        

def day15(array, auto=True):
    interpreter = IntcodeInterpreter(array)
    interpreter.set_infinite_memory(True)
    if not auto:
        day15_manual(interpreter)
    
    tile_map = [[" " for _ in range(41)] for _ in range(41)]
    curr_row = 21
    curr_col = 21
    directions = {1:(-1,0), 4:(0,1), 2:(1,0), 3:(0,-1)}
    reversed_directions = {1:2, 2:1, 3:4, 4:3}

    movement_from_start_stack = []
    visited_coords = set()

    oxy_row = -1
    oxy_col = -1

    while True:
        curr_coords = (curr_row, curr_col)
        if curr_coords not in visited_coords:
            visited_coords.add((curr_row, curr_col))
            for d in directions:
                input_stream = [d]
                output_stream = []
                interpreter.run(input_stream=input_stream, output_stream=output_stream)
                direction_vector = directions[d]
                next_row = curr_row + direction_vector[0]
                next_col = curr_col + direction_vector[1]
                
                if output_stream[0] == 0:
                    tile_map[next_row][next_col] = '#'
                    visited_coords.add((next_row, next_col))
                elif output_stream[0] == 1:
                    tile_map[next_row][next_col] = '.'
                    input_stream = [reversed_directions[d]]
                    interpreter.run(input_stream=input_stream, output_stream=[])
                elif output_stream[0] == 2:
                    tile_map[next_row][next_col] = 'O'
                    print("Part 1:", len(movement_from_start_stack) + 1)
                    input_stream = [reversed_directions[d]]
                    interpreter.run(input_stream=input_stream, output_stream=[])
                    oxy_row = next_row
                    oxy_col = next_col
        
        moved = False
        for d in directions:
            direction_vector = directions[d]
            next_row = curr_row + direction_vector[0]
            next_col = curr_col + direction_vector[1]
            next_coords = (next_row, next_col)
            if next_coords in visited_coords:
                continue
            else:
                moved = True
                movement_from_start_stack.append(d)
                curr_row = next_row
                curr_col = next_col
                input_stream = [d]
                interpreter.run(input_stream=input_stream, output_stream=[])
                break

        if not moved:
            if len(movement_from_start_stack) == 0:
                break
            movement = movement_from_start_stack.pop()
            reversed_movement = reversed_directions[movement]
            input_stream = [reversed_movement]
            interpreter.run(input_stream=input_stream, output_stream=[])
            direction_vector = directions[reversed_movement]
            curr_row = curr_row + direction_vector[0]
            curr_col = curr_col + direction_vector[1]
    
    
    print("Part 2:", get_time_for_oxy_to_fill(tile_map, oxy_row, oxy_col))
    
if __name__ == "__main__":
    filename = "input15.txt"
    arr = arrayise(filename)
    arr = arr[0].split(',')
    arr = [int(i) for i in arr]
    day15(arr, auto=True)
    

