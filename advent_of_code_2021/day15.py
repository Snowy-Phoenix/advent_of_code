import math
import re
import numpy as np
import copy
import itertools
import heapq

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day15a(array):
    risks = dict()
    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    cavern = []
    for i in range(len(array)):
        cavern.append([])
        for n in range(len(array[i])):
            cavern[i].append(int(array[i][n]))

    risks[(0,0)] = 0

    coords_to_check = set()
    coords_to_check.add((0,0))
    

    finished_coords = set()
    
    while True:
        if len(coords_to_check) == 0:
            break
        lowest_risk = 2**31
        current_coords = None
        for coords in coords_to_check:
            if risks[coords] < lowest_risk:
                lowest_risk = risks[coords]
                current_coords = coords
        coords_to_check.remove(current_coords)
        
        curr_row, curr_col = current_coords
        current_risk = risks[current_coords]

        for d in directions:
            next_row = curr_row + d[0]
            next_col = curr_col + d[1]
            if next_row < 0 or next_row >= len(cavern):
                continue
            if next_col < 0 or next_col >= len(cavern[0]):
                continue
            
            next_coords = (next_row, next_col)
            tile_risk = cavern[next_row][next_col]

            if next_coords in finished_coords:
                continue

            if next_coords not in risks:
                risks[next_coords] = current_risk + tile_risk
            else:
                risks[next_coords] = min(risks[next_coords], current_risk + tile_risk)
                
            coords_to_check.add(next_coords)

        finished_coords.add(current_coords)
            

    print("Part 1:", risks[(len(cavern)-1, len(cavern[0])-1)])
        
def day15b(array):
    risks = dict()
    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    cavern = []
    for i in range(len(array) * 5):
        index_i = i % len(array)
        risk_add1 = i // len(array)
        cavern.append([])
        for j in range(len(array[index_i]) * 5):
            risk_add2 = j // len(array[index_i])
            index_j = j % len(array[index_i])

            calculated_risk = (((int(array[index_i][index_j]) - 1) + risk_add1 + risk_add2) % 9) + 1

            cavern[i].append(calculated_risk)
    
    risks[(0,0)] = 0

    coords_to_check = set()
    coords_to_check.add((0,0))
    

    finished_coords = set()

    while True:
        if len(coords_to_check) == 0:
            break
        lowest_risk = 2**31
        current_coords = None
        for coords in coords_to_check:
            if risks[coords] < lowest_risk:
                lowest_risk = risks[coords]
                current_coords = coords
        coords_to_check.remove(current_coords)
        
        curr_row, curr_col = current_coords
        current_risk = risks[current_coords]

        for d in directions:
            next_row = curr_row + d[0]
            next_col = curr_col + d[1]
            if next_row < 0 or next_row >= len(cavern):
                continue
            if next_col < 0 or next_col >= len(cavern[0]):
                continue
            
            next_coords = (next_row, next_col)
            tile_risk = cavern[next_row][next_col]

            if next_coords in finished_coords:
                continue

            if next_coords not in risks:
                risks[next_coords] = current_risk + tile_risk
            else:
                risks[next_coords] = min(risks[next_coords], current_risk + tile_risk)
                
            coords_to_check.add(next_coords)
        
        finished_coords.add(current_coords)
            

    print("Part 2:", risks[(len(cavern)-1, len(cavern[0])-1)])

if __name__ == "__main__":
    filename = "input15.txt"
    arr = arrayise(filename)
    day15a(arr)
    day15b(arr)

