import math
import re
import numpy as np
import copy
import itertools
import time

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def dice1():
    current_n = 1
    while True:
        yield current_n
        current_n += 1
        if current_n > 100:
            current_n = 1

def dice2():
    for d1 in range(1, 4):
        for d2 in range(1, 4):
            for d3 in range(1, 4):
                yield d1 + d2 + d3

def day21a(array):
    p1_position = int(re.fullmatch(".+1.+(\\d+)", array[0]).group(1)) - 1
    p2_position = int(re.fullmatch(".+2.+(\\d+)", array[1]).group(1)) - 1
    p1_score = 0
    p2_score = 0

    track = [x for x in range(1, 11)]

    dice_rolls = 0
    p1_turn = True
    dice = dice1()
    while p1_score < 1000 and p2_score < 1000:
        spaces_moved = 0
        if p1_turn:
            for _ in range(3):
                spaces_moved += dice.__next__()
            p1_position = (p1_position + spaces_moved) % len(track)
            p1_score += track[p1_position]
        else:
            for _ in range(3):
                spaces_moved += dice.__next__()
            p2_position = (p2_position + spaces_moved) % len(track)
            p2_score += track[p2_position]
        dice_rolls += 3
        p1_turn = not p1_turn
    print("Part 1:", min(p1_score, p2_score) * dice_rolls)


def day21b(array):
    p1_position = int(re.fullmatch(".+1.+(\\d+)", array[0]).group(1)) - 1
    p2_position = int(re.fullmatch(".+2.+(\\d+)", array[1]).group(1)) - 1
    p1_wins = 0
    p2_wins = 0

    track = [x for x in range(1, 11)]

    max_score = 21
    curr_states = {(0, p1_position, 0, p2_position, True): 1}
    next_states = dict()
    while len(curr_states) > 0:
        for state in curr_states:
            curr_p1_score = state[0]
            curr_p1_pos = state[1]
            curr_p2_score = state[2]
            curr_p2_pos = state[3]
            is_p1_turn = state[4]
            curr_count = curr_states[state]
            if is_p1_turn:
                for spaces_moved in dice2():
                    next_position = (curr_p1_pos + spaces_moved) % len(track)
                    next_score = curr_p1_score + track[next_position]
                    if next_score >= max_score:
                        p1_wins += curr_count
                        continue
                    next_state = (next_score, next_position, curr_p2_score, curr_p2_pos, False)
                    if next_state in next_states:
                        next_states[next_state] += curr_count
                    else:
                        next_states[next_state] = curr_count
            else:
                for spaces_moved in dice2():
                    next_position = (curr_p2_pos + spaces_moved) % len(track)
                    next_score = curr_p2_score + track[next_position]
                    if next_score >= max_score:
                        p2_wins += curr_count
                        continue
                    next_state = (curr_p1_score, curr_p1_pos, next_score, next_position, True)
                    if next_state in next_states:
                        next_states[next_state] += curr_count
                    else:
                        next_states[next_state] = curr_count
        curr_states = next_states
        next_states = dict()

    print("Part 2:", max(p1_wins, p2_wins))


if __name__ == "__main__":
    filename = "input21.txt"
    arr = arrayise(filename)
    day21a(arr)
    day21b(arr)
    
