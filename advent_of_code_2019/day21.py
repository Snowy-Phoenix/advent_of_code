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

def day21(array):
    interpreter = IntcodeInterpreter(array)
    interpreter.set_infinite_memory(True)
    interpreter.print_ascii_output = True
    instructions = """NOT A T
NOT B J
OR J T
NOT C J
OR T J
AND D J
WALK
"""
    input_stream = []
    for c in instructions:
        input_stream.append(ord(c))
    interpreter.run(input_stream=input_stream)

    instructions = """NOT B T
NOT C J
OR T J
AND D J
AND H J
NOT A T
OR T J
RUN
"""
    input_stream = []
    for c in instructions:
        input_stream.append(ord(c))
    interpreter.run(input_stream=input_stream)



if __name__ == "__main__":
    filename = "input21.txt"
    arr = arrayise(filename)
    arr = arr[0].split(',')
    arr = [int(i) for i in arr]
    day21(arr)