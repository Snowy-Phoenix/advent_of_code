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

def day2(array):
    intcode = IntcodeInterpreter(array)
    intcode.set_infinite_memory(False)
    array[1] = 12
    array[2] = 2
    part1 = intcode.run(program=array) # 2782414
    print("Part 1:", intcode.run(program=array))
    assert part1 == 2782414

    desired_output = 19690720
    i = 0
    while True:
        array[1] = i
        j = 0
        while True:
            array[2] = j
            result = intcode.run(array)
            if result == desired_output:
                part2 = 100 * i + j
                print("Part 2:", part2)
                assert part2 == 9820
                return
            elif result == -1:
                break
            j += 1
        i += 1

if __name__ == "__main__":
    filename = "input2.txt"
    arr = arrayise(filename)
    arr = arr[0].split(',')
    arr = [int(i) for i in arr]
    
    day2(arr)
    

