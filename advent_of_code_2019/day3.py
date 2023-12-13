import math
import re
import numpy as np

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day3(array):
    wirepath1 = array[0].split(",")
    wirepath2 = array[1].split(",")
    visited_points_steps = dict() # dictionary of a tuple x and y, and steps
    direction_vectors = {"R":(1,0), "L":(-1,0), "U":(0,1), "D":(0,-1)}
    
    current_x = 0
    current_y = 0
    steps_taken = 0
    for path in wirepath1:
        direction = path[0]
        steps = int(path[1:])
        vector = direction_vectors[direction]
        for _ in range(steps):
            current_x += vector[0]
            current_y += vector[1]
            coords = (current_x, current_y)
            steps_taken += 1
            if coords not in visited_points_steps:
                visited_points_steps[coords] = steps_taken
    
    intersections = dict()
    current_x = 0
    current_y = 0
    steps_taken = 0
    for path in wirepath2:
        direction = path[0]
        steps = int(path[1:])
        vector = direction_vectors[direction]
        for _ in range(steps):
            current_x += vector[0]
            current_y += vector[1]
            coords = (current_x, current_y)
            steps_taken += 1
            if coords in visited_points_steps:
                if coords not in intersections:
                    intersections[coords] = steps_taken + visited_points_steps[coords]

    minimum_distance = 2**30
    for intersection in intersections:
        distance = abs(intersection[0]) + abs(intersection[1])
        if distance < minimum_distance:
            minimum_distance = distance
    print("Part 1:", minimum_distance)

    print("Part 2:", min(intersections.values()))

if __name__ == "__main__":
    filename = "input3.txt"
    arr = arrayise(filename)
    day3(arr)
    

