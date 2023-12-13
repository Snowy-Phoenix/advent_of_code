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

def process_packets(raw_packets, queue):
    for i in range(0, len(raw_packets), 3):
        computer_i = raw_packets[i]
        x = raw_packets[i + 1]
        y = raw_packets[i + 2]
        queue.append((computer_i, x, y))

def day23(array):
    interpreter = IntcodeInterpreter(array)
    interpreter.set_infinite_memory(True)
    interpreter.print_ascii_output = True
    computers = []
    packet_queue = deque()
    for i in range(50):
        interpreter = IntcodeInterpreter(array)
        interpreter.set_infinite_memory(True)
        interpreter.run(input_stream=[i])
        computers.append(interpreter)
    
    nat = [0, 0, True]
    start = True
    first_255 = True
    while True:
        if len(packet_queue) == 0:
            if start:
                for c in computers:
                    output = []
                    c.run(input_stream=[-1], output_stream=output)
                    process_packets(output, packet_queue)
                start = False
            else:
                if nat[2] == False:
                    print("Part 2:", nat[1])
                    break
                output = []
                computers[0].run(input_stream=[nat[0], nat[1]], output_stream=output)
                process_packets(output, packet_queue)
                nat[2] = False
        else:
            i, x, y = packet_queue.popleft()
            if i == 255:
                if first_255:
                    print("Part 1:", y)
                    first_255 = False
                if nat[0] != x or nat[1] != y:
                    nat[0] = x
                    nat[1] = y
                    nat[2] = True
                continue
            output = []
            computers[i].run(input_stream=[x, y], output_stream=output)
            process_packets(output, packet_queue)

if __name__ == "__main__":
    filename = "input23.txt"
    arr = arrayise(filename)
    arr = arr[0].split(',')
    arr = [int(i) for i in arr]
    day23(arr)