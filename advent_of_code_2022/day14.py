from collections import deque
from collections import defaultdict
import math

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def solve(arr):
    grid = set()
    max_rows = 0
    max_cols = 0
    for line in arr:
        line = line.split(' -> ')
        line_i = 1
        while line_i < len(line):
            to_coords = line[line_i]
            tocol, torow = tuple(map(int, to_coords.split(',')))
            from_coords = line[line_i - 1]
            fromcol, fromrow = tuple(map(int, from_coords.split(',')))
            max_rows = max(max_rows, fromrow, torow)
            max_cols = max(max_cols, fromcol, tocol)
            assert tocol == fromcol or torow == fromrow
            if (tocol - fromcol != 0):
                for i in range(tocol, fromcol + (tocol < fromcol)*2 - 1, (tocol < fromcol)*2 - 1):
                    grid.add((torow, i))
            else:
                for i in range(torow, fromrow + (torow < fromrow)*2 - 1, (torow < fromrow)*2 - 1):
                    grid.add((i, tocol))
            line_i += 1
    sand_dropped = 0
    part1 = True
    while True:
        sand = [0, 500]
        if tuple(sand) in grid:
            print("Part 2:", sand_dropped)
            break
        while True:
            if sand[0] >= max_rows + 1:
                if part1:
                    print("Part 1:", sand_dropped)
                    part1 = False
                grid.add((sand[0], sand[1]))
                sand_dropped += 1
                break                
            else:
                if (sand[0] + 1, sand[1]) not in grid:
                    sand[0] += 1
                elif (sand[0] + 1, sand[1] - 1) not in grid:
                    sand[0] += 1
                    sand[1] -= 1
                elif (sand[0] + 1, sand[1] + 1) not in grid:
                    sand[0] += 1
                    sand[1] += 1 
                else:
                    grid.add(tuple(sand))
                    sand_dropped += 1
                    break

if __name__ == '__main__':
    filename = "input14.txt"
    arr = arrayise(filename)
    solve(arr)
