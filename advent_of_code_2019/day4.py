import math
import re
import numpy as np

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def verify1(n):
    n_str = str(n)
    has_double = False
    for i in range(1, len(n_str)):
        if n_str[i] == n_str[i - 1]:
            has_double = True
        elif n_str[i - 1] > n_str[i]:
            return False
    return has_double

def verify2(n):
    n_str = str(n)
    counts = dict()
    for i in range(len(n_str)):

        if n_str[i] in counts:
            counts[n_str[i]] += 1
        else:
            counts[n_str[i]] = 1

        if n_str[i - 1] > n_str[i] and i != 0:
            return False
    if 2 in counts.values():
        return True
    return False

def day4(array):
    minimum, maximum = array[0].split('-')
    minimum = int(minimum)
    maximum = int(maximum)
    valid_passwords1 = 0
    valid_passwords2 = 0
    for i in range(minimum, maximum + 1):
        valid_passwords1 += verify1(i)
        valid_passwords2 += verify2(i)
    print("Part 1:", valid_passwords1)
    print("Part 2:", valid_passwords2)
    

if __name__ == "__main__":
    filename = "input4.txt"
    arr = arrayise(filename)
    day4(arr)
    

