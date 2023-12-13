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

def day17(array):
    coordinates = array[0].split(": ")[1]
    target_x_range, target_y_range = coordinates.split(", ")
    min_target_x, max_target_x  = target_x_range.split("..")
    min_target_x = int(min_target_x[2:])
    max_target_x = int(max_target_x)

    min_target_y, max_target_y  = target_y_range.split("..")
    min_target_y = int(min_target_y[2:])
    max_target_y = int(max_target_y)

    max_y_initial_velocity = 0
    testing_y_velocity = min_target_y
    valid_y_velocities = 0
    while testing_y_velocity < 1000:
        simulated_y_velocity = testing_y_velocity
        y_coords = 0
        while min_target_y <= y_coords:
            y_coords += simulated_y_velocity
            simulated_y_velocity -= 1

            if min_target_y <= y_coords <= max_target_y:
                max_y_initial_velocity = testing_y_velocity
                valid_y_velocities
        testing_y_velocity += 1
    max_height = (max_y_initial_velocity * (max_y_initial_velocity + 1)) // 2
    print("Part 1:", max_height)

    valid_velocities = set()
    for testing_x_velocity in range(0, max_target_x + 1):
        for testing_y_velocity in range(min_target_y, max_y_initial_velocity + 1):
            simulated_x = testing_x_velocity
            simulated_y = testing_y_velocity
            x_coords = 0
            y_coords = 0
            while True:
                if x_coords > max_target_x:
                    break
                if y_coords < min_target_y:
                    break
                x_coords += simulated_x
                y_coords += simulated_y
                if simulated_x > 0:
                    simulated_x -= 1
                simulated_y -= 1
                if min_target_x <= x_coords <= max_target_x:
                    if min_target_y <= y_coords <= max_target_y:
                        valid_velocities.add((testing_x_velocity, testing_y_velocity))
                        break
    print("Part 2:", len(valid_velocities))

if __name__ == "__main__":
    filename = "input17.txt"
    arr = arrayise(filename)
    # testcases = arrayise("test_cases.txt")
    day17(arr)

