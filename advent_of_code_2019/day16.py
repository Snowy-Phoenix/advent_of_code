import math
import re
import numpy as np
import itertools
import time


def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def sign(digit_position, line_number):
    cycle = (line_number + 1) * 4
    position_in_cycle = (digit_position % cycle) + 1
    block_position_in_cycle = position_in_cycle // (line_number + 1)
    if block_position_in_cycle % 2 == 0:
        return 0
    elif block_position_in_cycle == 1:
        return 1
    else:
        return -1

def day16a(array):
    number_array = []
    for n in array[0]:
        number_array.append(int(n))
    
    new_number_array = []
    for phases in range(100):
        for line_number in range(len(number_array)):
            cumsum = 0
            if line_number > len(number_array) // 2:
                cumsum = sum(number_array[line_number: len(number_array)])
            else:
                position = line_number
                curr_sign = 1
                block_length_left = line_number + 1
                while position < len(number_array):
                    if block_length_left == 1:
                        cumsum += curr_sign * number_array[position]
                        position += line_number + 2
                        block_length_left = line_number + 1
                        curr_sign *= -1
                    else:
                        cumsum += curr_sign * number_array[position]
                        position += 1
                        block_length_left -= 1
            new_digit = abs(cumsum) % 10
            new_number_array.append(new_digit)
        number_array = new_number_array
        new_number_array = []
    
    final_number = 0
    for i in range(8):
        final_number *= 10
        final_number += number_array[i]
    print("Part 1:", final_number)

def day16b(array):
    half = (len(array[0]) * 10000) // 2
    offset = 0
    for i in range(7):
        offset *= 10
        offset += int(array[0][i])
    
    number_array = []
    for i in range(offset, len(array[0]) * 10000):
        number_array.append(int(array[0][i % len(array[0])]))
    if offset < half:
        print("Unable to find hidden message.")
        return
    new_number_array = []
    for phases in range(100):
        cumsum = 0
        for i in range(len(number_array) - 1, -1, -1):
            cumsum += number_array[i]
            new_number_array.append(cumsum)
        for i in range(len(new_number_array)):
            number_array[len(number_array) - 1 - i] = new_number_array[i] % 10
        new_number_array = []

    final_number = 0
    for i in range(8):
        final_number *= 10
        final_number += number_array[i]
    print("Part 2:", final_number)


if __name__ == "__main__":
    filename = "input16.txt"
    arr = arrayise(filename)
    
    day16a(arr)
    day16b(arr)

