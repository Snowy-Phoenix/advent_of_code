import math
import re
import numpy as np

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day10(arr):
    bracket_pairs = {"(":")", "[":"]", "{":"}", "<":">"}
    bracket_val = {")":3, "]":57, "}":1197, ">":25137}
    total_error = 0

    uncorrupted_lines_scores = []
    score_dict = {"(":1, "[":2, "{":3, "<":4}
    
    for line in arr:
        total_score = 0
        stack = []
        corrupted = False
        for char in line:
            if char in bracket_pairs:
                stack.append(char)
            else:
                c = stack.pop()
                if bracket_pairs[c] != char:
                    total_error += bracket_val[char]
                    corrupted = True
                    break
        if not corrupted:
            while len(stack) > 0:
                char = stack.pop()
                total_score *= 5
                total_score += score_dict[char]
            uncorrupted_lines_scores.append(total_score)
    uncorrupted_lines_scores = sorted(uncorrupted_lines_scores)
    print("Part 1:", total_error)
    print("Part 2:", uncorrupted_lines_scores[len(uncorrupted_lines_scores)//2])


if __name__ == "__main__":
    filename = "input10.txt"
    arr = arrayise(filename)
    day10(arr)

