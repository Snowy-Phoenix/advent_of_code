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

def is_colliding(grid, x, y, shape):
    
    for coords in shape:
        sx, sy = coords
        if (x + sx < 0 or x + sx > 6):
            return True
        if y + sy <= 0:
            return True

        if (x + sx, y + sy) in grid:
            return True

    return False

def solve(arr):
    gas = arr[0]
    print(len(gas))
    ih_shape = ((0, 0), (1,0), (2,0), (3,0))
    plus_shape = ((1,0), (0,1), (1,1), (2,1), (1,2))
    bigl_shape = ((0,0),(1,0),(2,0),(2,1),(2,2))
    iv_shape = ((0,0), (0,1), (0,2), (0,3))
    o_shape = ((0,0), (0,1), (1,0), (1,1))
    shapes = [ih_shape, plus_shape, bigl_shape, iv_shape, o_shape]

    seen_permutations = dict() # (shape_i, gas_i, (tops of all)) : times seen
    cols = [0,0,0,0,0,0,0]
    col_diffs = [0,0,0,0,0,0,0]
    permutation_loop = False
    found_cycle = False
    permutation_cycle_offset = 0
    initial_rock_height = 0

    permutation_cycle = 0
    first_duplicate = None
    cycle_rock_height = 0
    heights = []

    gas_i = 0
    rock_height = 0
    shape_i = 0
    grid = set() # (x, y)
    shape_coords = [2, 4]
    rocks_settled = 0
    while True:
        c = gas[gas_i]
        shape = shapes[shape_i]
        if c == '>':
            if not is_colliding(grid, shape_coords[0] + 1, shape_coords[1], shape):
                shape_coords[0] += 1
        else:
            if not is_colliding(grid, shape_coords[0] - 1, shape_coords[1], shape):
                shape_coords[0] -= 1
        if is_colliding(grid, shape_coords[0], shape_coords[1] - 1, shape):
            for offset in shape:
                x, y = offset
                rock_height = max(rock_height, shape_coords[1] + y)
                assert (shape_coords[0] + x, shape_coords[1] + y) not in grid
                grid.add((shape_coords[0] + x, shape_coords[1] + y))
                cols[shape_coords[0] + x] = max(cols[shape_coords[0] + x], shape_coords[1] + y)
            
            rocks_settled += 1
            if rocks_settled == 2022:
                print("Part 1:", rock_height)
            elif rocks_settled == 1000000000000:
                print("Part 2: ", rock_height)
            shape_i = (shape_i + 1) % len(shapes)
            shape_coords = [2, rock_height + 4]

            min_col = min(cols)
            for i in range(len(cols)):
                col_diffs[i] = (cols[i] - min_col)
            permutation = (shape_i, gas_i, tuple(col_diffs))
            if permutation in seen_permutations:
                seen_permutations[permutation] += 1
                if not permutation_loop:
                    permutation_cycle_offset = rocks_settled + 1
                    initial_rock_height = rock_height
                    permutation_loop = True
                    first_duplicate = permutation
                elif not found_cycle:
                    if permutation == first_duplicate:
                        permutation_cycle += 1
                        found_cycle = True
                        cycle_rock_height = rock_height - initial_rock_height
                        break
                    else:
                        permutation_cycle += 1
                        heights.append(rock_height - initial_rock_height)
            else:
                assert permutation_loop == False
                seen_permutations[permutation] = 1
        else:
            shape_coords[1] -= 1
        gas_i = (gas_i + 1) % len(gas)

    simulations = 1000000000000

    # Add the initial rock height.
    simulations -= permutation_cycle_offset
    total_rock_height = initial_rock_height

    # get the total number of cycles undergone.
    total_cycles = simulations // permutation_cycle
    total_rock_height += total_cycles * cycle_rock_height

    # Get the remainder.
    remainder = simulations % permutation_cycle
    total_rock_height += heights[remainder]
    print("Part 2:", total_rock_height)


if __name__ == '__main__':
    filename = "input17.txt"
    arr = arrayise(filename)
    solve(arr)
    