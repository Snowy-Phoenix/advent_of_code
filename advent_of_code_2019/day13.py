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

def day13(array, manual_play=True):
    array[0] = 2
    interpreter = IntcodeInterpreter(array)
    interpreter.set_infinite_memory(True)
    is_first_line = True
    current_score = 0
    input_stream = [0]
    ball_x = 0
    paddle_x = 0
    steps = 0
    while not interpreter.halted:
        output_stream = []
        interpreter.run(input_stream=input_stream, output_stream=output_stream)
        x_coords = []
        y_coords = []
        tile_id = []
        
        i = 0
        while i < len(output_stream):
            value = output_stream[i]
            if value == -1:
                current_score = output_stream[i + 2]
                i += 2
            elif i % 3 == 0:
                x_coords.append(value)
            elif i % 3 == 1:
                y_coords.append(value)
            else:
                tile_id.append(value)
            i += 1
        
        if is_first_line:
            max_x = max(x_coords)
            max_y = max(y_coords)
            tile_map = [[' ' for x in range(max_x + 1)] for y in range(max_y + 1)]
        
        num_blocks = 0
        for i in range(len(tile_id)):
            x = x_coords[i]
            y = y_coords[i]
            tile = tile_id[i]
            if tile == 0:
                tile_map[y][x] = ' '
            elif tile == 1:
                # Indestructible walls
                tile_map[y][x] = '#'
            elif tile == 2:
                # Destructible walls (blocks)
                num_blocks += 1
                tile_map[y][x] = '='
            elif tile == 3:
                # Horizontal paddle
                tile_map[y][x] = '-'
                paddle_x = x
            elif tile == 4:
                # Ball
                tile_map[y][x] = 'O'
                ball_x = x
        if is_first_line:
            print("Part 1:", num_blocks)
            is_first_line = False
        
        screen = ""
        for row in tile_map:
            for col in row:
                screen += col
            screen += '\n'
        
        # if steps % 100 == 0 or manual_play:
        #     print("Score:", current_score)
        #     print(screen)
        if manual_play:
            user_input = input()
            if user_input == 'a':
                input_stream = [-1]
                print(user_input)
            elif user_input == 'd':
                input_stream = [1]
            else:
                input_stream = [0]
        else:
            if ball_x < paddle_x:
                input_stream = [-1]
            elif ball_x > paddle_x:
                input_stream = [1]
            else:
                input_stream = [0]


        steps += 1
    # print(screen)
    print("Part 2 score:", current_score)

if __name__ == "__main__":
    filename = "input13.txt"
    arr = arrayise(filename)
    arr = arr[0].split(',')
    arr = [int(i) for i in arr]
    day13(arr, manual_play=False)
    

