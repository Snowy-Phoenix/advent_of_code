import re
import numpy as np
import copy

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day25(array):
    card_public_key = int(array[0])
    door_public_key = int(array[1])
    subject_number = 7

    value = 1
    loop_size = 0
    card_secret_loop = 0
    door_secret_loop = 0
    while door_secret_loop == 0 or card_secret_loop == 0:
        value *= subject_number
        value %= 20201227
        loop_size += 1
        if value == card_public_key:
            card_secret_loop = loop_size
        if value == door_public_key:
            door_secret_loop = loop_size
    print(card_secret_loop, door_secret_loop)
    encryption_key1 = 1
    for i in range(card_secret_loop):
        encryption_key1 *= door_public_key
        encryption_key1 %= 20201227
    print("Using card:", encryption_key1)
    encryption_key2 = 1
    for i in range(door_secret_loop):
        encryption_key2 *= card_public_key
        encryption_key2 %= 20201227
    print("Using door:", encryption_key2)

if __name__ == "__main__":
    filename = "input25.txt"
    arr = arrayise(filename)
    day25(arr)
