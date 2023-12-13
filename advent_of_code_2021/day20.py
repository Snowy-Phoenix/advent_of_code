import math
import re
import numpy as np
import copy
import itertools
import time

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def pad_image(image, is_dark):
    char = '#'
    if is_dark:
        char = '.'
    for row in image:
        row.insert(0, char)
        row.append(char)
    front = [char for _ in range(len(image[0]))]
    end = [char for _ in range(len(image[0]))]
    image.insert(0, front)
    image.append(end)

def get_output_pixel(image, row, col, algorithm, background_is_dark):
    background_constant = int(not background_is_dark)
    binary_number = 0
    for i in range(3):
        for j in range(3):
            observed_row = row - 1 + i
            observed_col = col - 1 + j
            binary_number = binary_number << 1
            if observed_row < 0 or observed_row >= len(image):
                binary_number += background_constant
            elif observed_col < 0 or observed_col >= len(image[observed_row]):
                binary_number += background_constant
            else:
                tile = image[observed_row][observed_col]
                if tile == '#':
                    binary_number += 1
    return algorithm[binary_number]

def print_image(image):
    image_str = ""
    for row in image:
        for c in row:
            image_str += c
        image_str += '\n'
    print(image_str)

def count_lit(image):
    num_lit = 0
    for row in image:
        for pixel in row:
            if pixel == '#':
                num_lit += 1
    return num_lit

def day20(array, display_output=False):
    image_enhancement_algorithm = array[0]
    curr_image = []
    for i in range(2, len(array)):
        curr_image.append([])
        row = array[i]
        for c in row:
            curr_image[-1].append(c)
    
    black_to_white = False
    white_to_black = False
    if image_enhancement_algorithm[0] == '#':
        black_to_white = True
    if image_enhancement_algorithm[1] == '.':
        white_to_black = True
    
    is_curr_background_black = True
    for iteration in range(50):
        pad_image(curr_image, is_curr_background_black)
        output_image = []
        for r in range(len(curr_image)):
            output_image.append([])
            for c in range(len(curr_image[r])):
                output_image[r].append(get_output_pixel(curr_image, r, c, image_enhancement_algorithm, is_curr_background_black))
        curr_image = output_image
        if is_curr_background_black:
            if black_to_white:
                is_curr_background_black = False
        else:
            if white_to_black:
                is_curr_background_black = True
        if iteration == 2:
            print("Part 1:", count_lit(curr_image))
        if display_output:
            print_image(curr_image)
            time.sleep(1)
            
    print("Part 2:", count_lit(curr_image))

if __name__ == "__main__":
    filename = "input20.txt"
    arr = arrayise(filename)
    day20(arr, display_output=False)
    
