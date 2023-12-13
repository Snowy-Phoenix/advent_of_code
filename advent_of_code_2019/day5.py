import math
import re
import numpy as np
from intcode import IntcodeInterpreter

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day5(array):
    interpreter = IntcodeInterpreter(array)
    interpreter.set_infinite_memory(False)
    print("Part 1:")

    output = interpreter.run(input_stream=[1], output_stream=[])
    expected = (0,0,0,0,0,0,0,0,0,6731945)
    print(output)
    assert tuple(output) == expected

    print("\nPart 2:")
    result = interpreter.run(input_stream=[5], output_stream=[])
    print(result[0])
    assert result[0] == 9571668
    # print(interpreter.memory)

if __name__ == "__main__":
    filename = "input5.txt"
    arr = arrayise(filename)
    arr = arr[0].split(',')
    arr = [int(i) for i in arr]
    day5(arr)
    

