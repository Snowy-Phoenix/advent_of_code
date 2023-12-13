from collections import deque
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

def day25(array):
    interpreter = IntcodeInterpreter(array)
    interpreter.set_infinite_memory(True)
    interpreter.print_ascii_output = True
    interpreter.run(input_stream=[])
    while True:
        input_str = input()
        if input_str == 'quit':
            break
        input_int = [ord(i) for i in input_str]
        input_int.append(10)
        interpreter.run(input_stream=input_int)

if __name__ == "__main__":
    filename = "input25.txt"
    arr = arrayise(filename)
    arr = arr[0].split(',')
    arr = [int(i) for i in arr]
    # Planetoid, pointer, sand, wreath
    day25(arr)