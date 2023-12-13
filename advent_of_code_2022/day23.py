from collections import deque
from collections import defaultdict
import heapq
import copy
import math

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip('\n'))
    return array

class Vector:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def __add__(self, other):
        if isinstance(other, tuple):
            return (self.row + other[0], self.col + other[1])
        return Vector(self.row + other.row, self.col + other.col)
            
    def __sub__(self, other):
        if isinstance(other, tuple):
            return (self.row - other[0], self.col - other[1])
        return Vector(self.row - other.row, self.col - other.col)

class Elf:
    null = Vector(0, 0)
    north = Vector(-1, 0)
    south = Vector(1,0)
    east = Vector(0,1)
    west = Vector(0,-1)
    ne = north + east
    nw = north + west
    se = south + east
    sw = south + west

    def __init__(self, coords):
        self.directions = ['N', 'S', 'W', 'E']
        self.coords = coords

    def shift_move(self):
        d = self.directions.pop(0)
        self.directions.append(d)
    
    def get_next_move(self, coords, grid):
        if ((Elf.north + coords in grid)
            or Elf.ne + coords in grid
            or Elf.nw + coords in grid
            or Elf.east + coords in grid
            or Elf.west + coords in grid
            or Elf.se + coords in grid
            or Elf.sw + coords in grid
            or Elf.south + coords in grid):
            for d in self.directions:
                if d == 'N':
                    if ((Elf.north + coords not in grid) 
                        and (Elf.nw + coords not in grid)
                        and (Elf.ne + coords not in grid)):
                        # self.directions.remove('N')
                        # self.directions.append('N')
                        self.shift_move()
                        return Elf.north
                elif d == 'E':
                    if ((Elf.east + coords not in grid) 
                        and (Elf.ne + coords not in grid)
                        and (Elf.se + coords not in grid)):
                        # self.directions.remove('E')
                        # self.directions.append('E')
                        self.shift_move()
                        return Elf.east
                elif d == 'W':
                    if ((Elf.west + coords not in grid) 
                        and (Elf.nw + coords not in grid)
                        and (Elf.sw + coords not in grid)):
                        # self.directions.remove('W')
                        # self.directions.append('W')
                        self.shift_move()
                        return Elf.west
                elif d == 'S':
                    if ((Elf.south + coords not in grid) 
                        and (Elf.se + coords not in grid)
                        and (Elf.sw + coords not in grid)):
                        # self.directions.remove('S')
                        # self.directions.append('S')
                        self.shift_move()
                        return Elf.south
        self.shift_move()
        return Elf.null

    def __repr__(self):
        return str(self.coords)

def print_grid(grid):
    minrow = 1 << 31
    maxrow = 0
    mincol = 1 << 31
    maxcol = 0
    for coords in grid:
        minrow = min(minrow, coords[0])
        maxrow = max(maxrow, coords[0])
        mincol = min(mincol, coords[1])
        maxcol = max(maxcol, coords[1])
    for row in range(minrow, maxrow + 1, 1):
        for col in range(mincol, maxcol + 1, 1):
            if (row, col) in grid:
                print("#", end='')
            else:
                print(".", end='')
        print()
    print()
def solve(arr):
    elves = dict() # coords, elf object
    for row, line in enumerate(arr):
        for col, char in enumerate(line):
            if char == '#':
                elves[(row, col)] = Elf((row, col))
    next_elves = dict()
    rounds = 0
    while True:
        if rounds == 10:
            minrow = 1 << 31
            maxrow = 0
            mincol = 1 << 31
            maxcol = 0
            for coords in elves:
                minrow = min(minrow, coords[0])
                maxrow = max(maxrow, coords[0])
                mincol = min(mincol, coords[1])
                maxcol = max(maxcol, coords[1])
            print("Part 1:", (maxrow - minrow + 1) * (maxcol - mincol + 1) - len(elves))
        next_elves.clear()
        changed = False
        for coords in elves:
            elf = elves[coords]
            vector = elf.get_next_move(coords, elves)
            if vector.row != 0 or vector.col != 0:
                changed = True
            next_coords = vector + coords
            if next_coords in next_elves:
                if next_elves[next_coords] != None:
                    conflicting_elf = next_elves[next_coords]
                    next_elves[next_coords] = None
                    next_elves[conflicting_elf.coords] = conflicting_elf
                next_elves[coords] = elf
            else:
                next_elves[next_coords] = elf
        if not changed:
            print("Part 2:", rounds + 1)
            return
        elves.clear()
        for coords in next_elves:
            if next_elves[coords] == None:
                continue
            elves[coords] = next_elves[coords]
            elves[coords].coords = coords
        # print_grid(elves)
        rounds += 1

if __name__ == '__main__':
    filename = "input23.txt"
    arr = arrayise(filename)
    solve(arr)
    