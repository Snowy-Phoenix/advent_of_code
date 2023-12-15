from collections import deque

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def tostr(grid):
    string = ''
    for r, line in enumerate(grid):
        for c, char in enumerate(line):
            string += char
        string += '\n'
    return string

def north(grid):
    for r, line in enumerate(grid):
        if (r == 0):
            continue
        for c, char in enumerate(line):
            if char == 'O':
                i = r - 1
                while i >= 0:
                    if grid[i][c] == '#' or grid[i][c] == 'O':
                        break
                    grid[i][c] = 'O'
                    grid[i + 1][c] = '.'
                    i -= 1
def west(grid):
    for c in range(len(grid[0])):
        for r in range(len(grid[0])):
            char = grid[r][c]
            if char == 'O':
                i = c - 1
                while i >= 0:
                    if grid[r][i] == '#' or grid[r][i] == 'O':
                        break
                    grid[r][i] = 'O'
                    grid[r][i + 1] = '.'
                    i -= 1
def east(grid):
    for c in range(len(grid[0]) - 1, -1, -1):
        for r in range(len(grid[0])):
            char = grid[r][c]
            if char == 'O':
                i = c + 1
                while i < len(grid[0]):
                    if grid[r][i] == '#' or grid[r][i] == 'O':
                        break
                    grid[r][i] = 'O'
                    grid[r][i - 1] = '.'
                    i += 1
def south(grid):
    for r in range(len(grid) - 1, -1, -1):
        if (r == len(grid) - 1):
            continue
        line = grid[r]
        for c, char in enumerate(line):
            if char == 'O':
                i = r + 1
                while i < len(grid):
                    if grid[i][c] == '#' or grid[i][c] == 'O':
                        break
                    grid[i][c] = 'O'
                    grid[i - 1][c] = '.'
                    i += 1

def solve(arr):
    grid = []
    for r, line in enumerate(arr):
        grid.append([])
        for c, char in enumerate(line):
            grid[-1].append(char)

    north(grid)
    
    i = 0
    for r, line in enumerate(grid):
        for c, char in enumerate(line):
            if char == 'O':
                i += len(grid) - r
    print(i)
    west(grid)
    south(grid)
    east(grid)
    hashmap = dict()
    max_cycles = 1000000000
    curr_cycle = 1
    transformations = [north, west, south, east]
    prev = tostr(grid)
    cycle_done = False
    cycle = []
    beg_cycle = ''
    while curr_cycle < max_cycles:
        if prev in hashmap:
            if not cycle_done:
                if prev == beg_cycle:
                    cycle_done = True
                    passes = max_cycles - curr_cycle
                    prev = cycle[passes % len(cycle)]
                    break
                else:
                    cycle.append(prev)
                    if beg_cycle == '':
                        beg_cycle = prev
                    prev = hashmap[prev]
                    curr_cycle += 1
        north(grid)
        west(grid)
        south(grid)
        east(grid)
        next = tostr(grid)
        hashmap[prev] = next
        prev = next
        curr_cycle += 1
    i = 0
    for r, line in enumerate(prev.strip().split('\n')):
        for c, char in enumerate(line):
            if char == 'O':
                i += len(grid) - r
    print(i)

if __name__ == '__main__':
    filename = "input14.txt"
    arr = arrayise(filename)
    solve(arr)