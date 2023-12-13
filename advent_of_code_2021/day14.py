from collections import defaultdict
import math
import re
import numpy as np
import copy
import itertools

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day14(array, iterations):
    polymer_template = array[0]
    insertion_rules = dict() # 
    for i in range(2, len(array)):
        line = array[i]
        pair, insertion = line.split(" -> ")
        insertion_rules[pair] = insertion
    
    pair_counts = dict()
    chars_counts = dict()

    for c in polymer_template:
        if c in chars_counts:
            chars_counts[c] += 1
        else:
            chars_counts[c] = 1

    for i in range(1, len(polymer_template)):
        c1 = polymer_template[i - 1]
        c2 = polymer_template[i]
        pair = c1 + c2

        if pair in pair_counts:
            pair_counts[pair] += 1
        else:
            pair_counts[pair] = 1
    
    

    old_pairs = pair_counts
    for i in range(iterations):
        new_pairs = dict()
        for pair in old_pairs:
            if pair in insertion_rules:
                inserted_char = insertion_rules[pair]
                
                if inserted_char in chars_counts:
                    chars_counts[inserted_char] += old_pairs[pair]
                else:
                    chars_counts[inserted_char] = old_pairs[pair]

                new_pair1 = pair[0] + inserted_char
                new_pair2 = inserted_char + pair[1]
                if new_pair1 in new_pairs:
                    new_pairs[pair[0] + inserted_char] += old_pairs[pair]
                else:
                    new_pairs[pair[0] + inserted_char] = old_pairs[pair]
                if new_pair2 in new_pairs:
                    new_pairs[inserted_char + pair[1]] += old_pairs[pair]
                else:
                    new_pairs[inserted_char + pair[1]] = old_pairs[pair]
            else:
                new_pairs[pair] = old_pairs[pair]
        old_pairs = new_pairs
    
    smallest = -1
    largest = -1
    for i in chars_counts:
        if smallest == -1:
            smallest = chars_counts[i]
            largest = chars_counts[i]
            continue
        smallest = min(smallest, chars_counts[i])
        largest = max(largest, chars_counts[i])
    
    print("{} steps: {}".format(iterations, largest - smallest))
    

if __name__ == "__main__":
    filename = "input14.txt"
    arr = arrayise(filename)
    day14(arr, 10)
    day14(arr, 40)

