import math
import re
import numpy as np

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day11(array, steps=100, include_diags=True):
    area = []
    for i in range(len(array)):
        area.append([])
        for c in array[i]:
            area[i].append(int(c))
    
    for i in area:
        i.insert(0, -2**31)
        i.append(-2**31)
    
    area.insert(0, [-2**31 for i in range(len(area[0]))])
    area.append([-2**31 for i in range(len(area[0]))])
    
    flashes = 0
    flashed_octopuses = set()
    i = 0
    while True:
        for r in range(1, len(area) - 1):
            for c in range(1, len(area[r]) - 1):
                flashes += flash(area, r, c, flashed_octopuses)
        flashed_octopuses.clear()
        for r in range(1, len(area)-1):
            for c in range(1, len(area)-1):
                if area[r][c] > 9:
                    area[r][c] = 0
        all_sync = True
        for r in range(1, len(area)-1):
            for c in range(1, len(area)-1):
                if area[r][c] != 0:
                    all_sync = False
                    break
        i += 1
        if i == steps:
            print("Part 1:", flashes)
        if all_sync:
            break
    print("Part 2:", i)


def flash(area, r, c, flashed_octopuses):
    flashes = 0
    area[r][c] += 1

    if area[r][c] > 9 and (r,c) not in flashed_octopuses:
        flashed_octopuses.add((r, c))
        flashes += 1
        flashes += flash(area, r-1,c+1, flashed_octopuses)
        flashes += flash(area, r-1,c, flashed_octopuses)
        flashes += flash(area, r-1,c-1, flashed_octopuses)

        flashes += flash(area, r,c+1, flashed_octopuses)
        flashes += flash(area, r,c-1, flashed_octopuses)

        flashes += flash(area, r+1,c+1, flashed_octopuses)
        flashes += flash(area, r+1,c, flashed_octopuses)
        flashes += flash(area, r+1,c-1, flashed_octopuses)

    return flashes

if __name__ == "__main__":
    filename = "input11.txt"
    arr = arrayise(filename)
    day11(arr)
    

