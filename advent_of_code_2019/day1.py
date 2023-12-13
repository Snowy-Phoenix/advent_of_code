import math
import re
import numpy as np

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def solve1(array):
    cumsum = 0
    for mass in array:
        cumsum += (mass // 3) - 2
    print("Part 1:", cumsum)

def solve2(array):
    cumsum = 0
    for mass in array:
        fuel_required = (mass // 3) - 2
        cumsum += fuel_required
        while True:
            fuel_required = (fuel_required // 3) - 2
            if fuel_required <= 0:
                break
            cumsum += fuel_required
    print("Part 2:", cumsum)

def day1(array):
    solve1(array)
    solve2(array)
    

if __name__ == "__main__":
    filename = "input1.txt"
    arr = arrayise(filename)
    arr = [int(i) for i in arr]
    day1(arr)
    

