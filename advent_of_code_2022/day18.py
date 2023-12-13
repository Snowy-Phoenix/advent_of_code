from collections import deque
from collections import defaultdict
import heapq
import copy
import math

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def solve(arr):
    cubes = set()
    surface = dict()
    orientations = [(0,0,1), (0,0,-1), (1,0,0), (-1,0,0), (0,1,0), (0,-1,0)]
    for line in arr:
        x,y,z = line.split(',')
        x = int(x)
        y = int(y)
        z = int(z)
        cubes.add((x,y,z))
        if (x,y,z) in surface:
            surface.pop((x,y,z))
        for face in orientations:
            point = (x + face[0], y + face[1], z + face[2])
            if (point in cubes):
                continue
            else:
                if point in surface:
                    surface[point] += 1
                else:
                    surface[point] = 1
    print("Part 1:", sum(surface.values()))

    maxx = 0
    maxy = 0
    maxz = 0
    minx = 1 << 31
    miny = 1 << 31
    minz = 1 << 31
    for point in surface:
        maxx = max(point[0], maxx)
        maxy = max(point[1], maxy)
        maxz = max(point[2], maxz)
        minx = min(point[0], minx)
        miny = min(point[1], miny)
        minz = min(point[2], minz)
    visited = set()
    fringe = list()
    fringe.append((minx, miny, minz))
    visited.add((minx, miny, minz))
    while len(fringe) > 0:
        coords = fringe.pop()
        for face in orientations:
            point = (coords[0] + face[0], coords[1] + face[1], coords[2] + face[2])
            if (point in cubes):
                continue
            if point in visited:
                continue
            if (point[0] < minx or maxx < point[0]):
                continue
            if (point[1] < miny or maxy < point[1]):
                continue
            if (point[2] < minz or maxz < point[2]):
                continue
            visited.add(point)
            fringe.append(point)
    outside_edges = visited.intersection(surface.keys())
    summation = 0
    for edge in outside_edges:
        summation += surface[edge]
    print("Part 2:", summation)



if __name__ == '__main__':
    filename = "input18.txt"
    arr = arrayise(filename)
    solve(arr)
    