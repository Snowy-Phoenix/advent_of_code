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

def day9(array):
    interpreter = IntcodeInterpreter(array)
    interpreter.set_infinite_memory(True)
    output1 = interpreter.run(program=array, input_stream=[1], output_stream=[])
    print("Part 1:", output1[0])
    assert output1[0] == 2436480432
    
    output2 = interpreter.run(program=array, input_stream=[2], output_stream=[])
    print("Part 2:", output2[0])
    assert output2[0] == 45710

        

if __name__ == "__main__":
    filename = "input9.txt"
    arr = arrayise(filename)
    arr = arr[0].split(',')
    arr = [int(i) for i in arr]
    day9(arr)
    

