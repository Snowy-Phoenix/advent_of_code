import math
import re
import numpy as np
import itertools
import time
from collections import defaultdict, deque

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    f.close()
    return array

def compute_biodiversity(grid):
    biodiversity = 0
    for r, row in enumerate(grid):
        for c, b in enumerate(row):
            biodiversity += b * (2 ** (r*len(grid) + c))
    return biodiversity

def simulate(grid):
    bug_count = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    vectors = [(1,0), (-1,0), (0,1), (0,-1)]
    for r, row in enumerate(grid):
        for c, b in enumerate(row):
            for v in vectors:
                new_r = r + v[0]
                new_c = c + v[1]
                if new_r < 0 or new_r >= len(grid):
                    continue
                if new_c < 0 or new_c >= len(row):
                    continue
                bug_count[new_r][new_c] += b
    for r, row in enumerate(grid):
        for c, b in enumerate(row):
            if b:
                if bug_count[r][c] != 1:
                    grid[r][c] = 0
            else:
                if 1 <= bug_count[r][c] <= 2:
                    grid[r][c] = 1

def day24a(array):
    grid = []
    for row in array:
        grid.append([])
        for c in row:
            if c == '#':
                grid[-1].append(1)
            else:
                grid[-1].append(0)
    grid = np.array(grid)
    seen = set()
    seen.add(compute_biodiversity(grid))
    while True:
        simulate(grid)
        biodiversity = compute_biodiversity(grid)
        if biodiversity in seen:
            print("Part 1:", biodiversity)
            break
        seen.add(biodiversity)

def add_bugs_recursive_room(bug, bug_counts, rows, cols):
    r = bug[0]
    c = bug[1]
    d = bug[2]
    if r == 1 and c == 2:
        for i in range(cols):
            bug_counts[(0, i, d + 1)] += 1
    elif r == 3 and c == 2:
        for i in range(cols):
            bug_counts[(rows - 1, i, d + 1)] += 1
    elif r == 2 and c == 1:
        for i in range(rows):
            bug_counts[(i, 0, d + 1)] += 1
    elif r == 2 and c == 3:
        for i in range(rows):
            bug_counts[(i, cols - 1, d + 1)] += 1


def day24b(array, minutes=200):
    rows = len(array)
    cols = len(array[0])
    bugs = set()
    for r, row in enumerate(array):
        for c, b in enumerate(row):
            if b == '#':
                bugs.add((r, c, 0))
    for _ in range(minutes):
        new_bugs = set()
        bug_counts = defaultdict(lambda: 0)
        vectors = ((1,0), (-1,0), (0,1), (0,-1))
        for b in bugs:
            for v in vectors:
                r = b[0] + v[0]
                c = b[1] + v[1]
                d = b[2]
                if r == -1:
                    bug_counts[(1, 2, d - 1)] += 1
                elif r == rows:
                    bug_counts[(3, 2, d - 1)] += 1
                elif c == -1:
                    bug_counts[(2, 1, d - 1)] += 1
                elif c == cols:
                    bug_counts[(2, 3, d - 1)] += 1
                elif r == 2 and c == 2:
                    add_bugs_recursive_room(b, bug_counts, rows, cols)
                else:
                    bug_counts[(r, c, d)] += 1
        for b in bug_counts:
            if bug_counts[b] == 1:
                new_bugs.add(b)
            elif bug_counts[b] == 2 and b not in bugs:
                new_bugs.add(b)
        bugs = new_bugs
    print("Part 2:", len(bugs))

if __name__ == "__main__":
    filename = "input24.txt"
    arr = arrayise(filename)
    day24a(arr)
    day24b(arr, 200)