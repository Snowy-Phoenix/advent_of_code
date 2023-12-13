import math
import re
import numpy as np
import itertools
import time
from collections import deque

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    f.close()
    return array

def cut(number, cards1, cards2):
    i1 = (len(cards1) + number) % len(cards1)
    i2 = 0
    while i2 != len(cards2):
        cards2[i2] = cards1[i1]
        i1 = (i1 + 1) % len(cards1)
        i2 += 1 

def deal_new_stack(cards1, cards2):
    i1 = len(cards1) - 1
    i2 = 0
    while i2 != len(cards2):
        cards2[i2] = cards1[i1]
        i1 -= 1
        i2 += 1

def deal_increment(increment, cards1, cards2):
    i1 = 0
    i2 = 0
    while i1 != len(cards1):
        cards2[i2] = cards1[i1]
        i1 += 1
        i2 = (i2 + increment) % len(cards2)

def shuffle(array, cards):
    shuffled = [i for i in range(len(cards))]
    for line in array:
        instructions = line.split()
        if instructions[0] == 'cut':
            cut(int(instructions[1]), cards, shuffled)
        elif instructions[-1] == 'stack':
            deal_new_stack(cards, shuffled)
        else:
            deal_increment(int(instructions[-1]), cards, shuffled)
        cards, shuffled = shuffled, cards
    return cards

def day22a(array, shuffles=1):
    num_cards = 10007
    cards = [i for i in range(num_cards)]
    for _ in range(shuffles):
        shuffle(array, cards)    
    print(cards.index(2019))

def track_cut(num_cards, position, cut):
    return (position - cut) % num_cards
def track_deal_stack(num_cards, position, _=0):
    return  (-position - 1) % num_cards
def track_deal_increment(num_cards, position, increment):
    return (position * increment) % num_cards

def day22b(array):
    
    offset = 0
    multiplier = 1
    num_cards = 10007

    instructions = []
    for line in array:
        instruction = line.split()
        if instruction[0] == 'cut':
            instructions.append((track_cut, int(instruction[1])))
            offset -= int(instruction[1])
        elif instruction[-1] == 'stack':
            instructions.append((track_deal_stack, 0))
            offset *= -1
            multiplier *= -1
            offset -= 1
        else:
            instructions.append((track_deal_increment, int(instruction[-1])))
            multiplier *= int(instruction[-1])
            offset *= int(instruction[-1])
    tracked_card = 2019
    shuffles = 1
    for _ in range(shuffles):
        for method, i in instructions:
            tracked_card = method(num_cards, tracked_card, i)
    print("Part 1:", tracked_card)
    multiplier %= num_cards
    offset %= num_cards
    shuffles = 12410
    tracked_card = 2018
    for _ in range(shuffles):
        tracked_card = (tracked_card * (multiplier) + offset) % num_cards
    print(tracked_card)
    

def day22c(array):
    offset = 0
    multiplier = 1
    offset_rev = 0
    multiplier_rev = 1
    num_cards = 10007
    for line in array:
        instruction = line.split()
        if instruction[0] == 'cut':
            offset -= int(instruction[1])
            offset_rev += int(instruction[1])
        elif instruction[-1] == 'stack':
            offset *= -1
            multiplier *= -1
            offset -= 1
            offset_rev *= -1
            multiplier_rev *= -1
            offset_rev -= 1
        else:
            multiplier *= int(instruction[-1])
            offset *= int(instruction[-1])
            multiplier_rev *=  -int(instruction[-1])
            offset_rev *= -int(instruction[-1])
    tracked_card = 2019
    multiplier1 = multiplier % num_cards
    offset1 = offset % num_cards
    print("Part 1:", (tracked_card * multiplier1 + offset1) % num_cards)

    tracked_card = 2020
    num_cards = 119315717514047
    shuffles = 101741582076661

    bin_representation = []
    current_num = shuffles
    while current_num > 0:
        bin_representation.append(current_num % 2)
        current_num = current_num >> 1

    curr_multiplier = multiplier
    curr_offset = offset
    cm = 1
    co = 0
    for bit in bin_representation:
        if bit == 1:
            cm = (cm * curr_multiplier) % num_cards
            co = (co * curr_multiplier + curr_offset) % num_cards
        curr_offset = curr_offset*(curr_multiplier + 1) % num_cards
        curr_multiplier = curr_multiplier**2 % num_cards
    inverse = pow(cm, -1, num_cards)
    print("Part 2:", ((tracked_card - co)*inverse) % num_cards)

if __name__ == "__main__":
    filename = "input22.txt"
    arr = arrayise(filename)
    # day22a(arr, 2)
    # day22b(arr)
    day22c(arr)