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

def day11a(array):
    interpreter = IntcodeInterpreter(array)
    interpreter.set_infinite_memory(True)

    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    current_direction = 0
    antx = 0
    anty = 0

    tile_map = dict() # Coordinates, is_white
    current_colour = 0
    while not interpreter.halted:
        output = []
        interpreter.run(input_stream=[current_colour], output_stream=output)
        painted_colour = output[0]
        turn = output[1]
        if turn == 0:
            current_direction = (current_direction - 1) % 4
        else:
            current_direction = (current_direction + 1) % 4
        
        tile_map[(antx, anty)] = bool(painted_colour)

        direction_vector = directions[current_direction]
        antx += direction_vector[0]
        anty += direction_vector[1]
        coords = (antx, anty)

        if coords not in tile_map:
            current_colour = 0
        else:
            current_colour = int(tile_map[coords])
    print("Part 1:", len(tile_map))
    print(get_final_image(tile_map))
        
        
def day11b(array):
    interpreter = IntcodeInterpreter(array)
    interpreter.set_infinite_memory(True)

    directions = [(0,1), (1,0), (0,-1), (-1,0)]
    current_direction = 0
    antx = 0
    anty = 0

    tile_map = {(0,0):True} # Coordinates, is_white
    current_colour = 1
    while not interpreter.halted:
        output = []
        interpreter.run(input_stream=[current_colour], output_stream=output)
        painted_colour = output[0]
        turn = output[1]
        if turn == 0:
            current_direction = (current_direction - 1) % 4
        else:
            current_direction = (current_direction + 1) % 4
        
        tile_map[(antx, anty)] = bool(painted_colour)

        direction_vector = directions[current_direction]
        antx += direction_vector[0]
        anty += direction_vector[1]
        coords = (antx, anty)

        if coords not in tile_map:
            current_colour = 0
        else:
            current_colour = int(tile_map[coords])
    trues = 0 
    for i in tile_map.values():
        if i:
            trues += 1

    string = get_final_image(tile_map)

    print("Part 2:")
    print(string)

def get_final_image(tile_map):
    max_x = -2**30
    min_x = 2**30
    max_y = -2**30
    min_y = 2**30
    for tile in tile_map:
        if tile[0] > max_x:
            max_x = tile[0]
        if tile[1] > max_y:
            max_y = tile[1]
        if tile[0] < min_x:
            min_x = tile[0]
        if tile[1] < min_y:
            min_y = tile[1]
    
    image = [[" " for _ in range(max_x - min_x + 1)] for _ in range(max_y - min_y + 1)]
    pounds = 0
    for r in range(max_y - min_y + 1):
        for c in range(max_x - min_x + 1):
            y = r + min_y
            x = c + min_x
            if (x, y) in tile_map:
                if tile_map[(x,y)]:
                    pounds += 1
                    image[r][c] = '#'
                else:
                    image[r][c] = ' '
            else:
                image[r][c] = ' '
    
    final_string = ""
    for r in range(len(image) - 1, -1, -1):
        row = image[r]
        for c in row:
            final_string += c
        final_string += '\n'
    return final_string

if __name__ == "__main__":
    filename = "input11.txt"
    arr = arrayise(filename)
    arr = arr[0].split(',')
    arr = [int(i) for i in arr]
    day11a(arr)
    day11b(arr)
    

