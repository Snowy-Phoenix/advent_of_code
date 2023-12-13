import math
import re
import numpy as np
import itertools

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day8(array):
    width = 25
    height = 6
    layer = width * height
    image = []
    string = array[0]
    for i in range(len(string)):
        row = i // layer
        if i % layer == 0:
            image.append([])
        image[row].append(string[i])
    
    counts = []
    for i in range(len(image)):
        row = image[i]
        zeros = 0
        ones = 0
        twos = 0
        for c in row:
            if c == '0':
                zeros += 1
            elif c == '1':
                ones += 1
            elif c == '2':
                twos += 1
            else:
                print(c)
        counts.append((zeros, ones, twos))
    
    fewest_zeros = -1
    fewest_zero_layer = None
    for layer in counts:
        if fewest_zeros == -1:
            fewest_zeros = layer[0]
            fewest_zero_layer = layer
        else:
            if layer[0] < fewest_zeros:
                fewest_zeros = layer[0]
                fewest_zero_layer = layer

    print("Part 1:", fewest_zero_layer[1] * fewest_zero_layer[2])
    final_image = []
    for i in range(len(image[0])):
        for layer in image:
            if layer[i] != '2':
                final_image.append(layer[i])
                break
    
    final_image_str = ""
    for i in range(len(final_image)):
        c = final_image[i]
        if i % width == 0:
            if final_image_str != "":
                final_image_str += "\n"
        if c == '0':
            final_image_str += " "
        else:
            final_image_str += "#"
    print("Part 2:")
    print(final_image_str)
        


    
if __name__ == "__main__":
    filename = "input8.txt"
    arr = arrayise(filename)
    day8(arr)
    

