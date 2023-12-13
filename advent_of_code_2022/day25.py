from collections import deque
from collections import defaultdict
import heapq
import copy
import math

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip('\n'))
    return array    

def snafu2decimal(snafu):
    digits = {'2':2, '1':1, '0':0, '-':-1, '=':-2}
    current_sum = 0
    for c in snafu:
        current_sum *= 5
        current_sum += digits[c]
    return current_sum

def decimal2snafu(decimal):
    digit2snafu = {0:'0', 1:'1', 2:'2', 3:'=', 4:'-'}
    snafu = ""
    carry = False
    while decimal > 0:
        digit = (decimal) % 5
        digit += int(carry)
        if digit < 3:
            carry = False
        else:
            carry = True
            digit = digit % 5
        snafu = digit2snafu[digit] + snafu
        decimal = decimal // 5
    if carry:
        snafu = digit2snafu[1] + snafu
        
    return snafu

def solve(arr):
    total_sum = 0
    for line in arr:
        total_sum += snafu2decimal(line)
    print("Part 1:", decimal2snafu(total_sum))
    

if __name__ == '__main__':
    filename = "input25.txt"
    arr = arrayise(filename)
    solve(arr)
    