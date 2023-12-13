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

class Tile:
    def __init__(self, char, coords):
        self.char = char
        self.coords = coords
        self.cube_coords = None
    def __repr__(self):
        return str((self.char, self.coords, self.cube_coords))

def estimate_cube_length(arr):
    lengths = []
    blanks = 0
    tiles = 0
    for line in arr:
        if line == '':
            break
        line_blanks = 0
        line_chars = 0
        for c in line:
            if c == ' ':
                line_blanks += 1
            else:
                line_chars += 1
        if blanks == 0 and tiles == 0:
            blanks = line_blanks
            tiles = line_chars
            lengths.append(1)
        else:
            if blanks != line_blanks or tiles != line_chars:
                lengths.append(1)
            else:
                lengths[-1] += 1
            blanks = line_blanks
            tiles = line_chars
    return min(lengths)

def fold_point(cutoff, axis_from, axis_to, cmp_is_below, fold_negative, point):
    sign = 1
    if fold_negative:
        sign = -1
    new_point = list(point)
    if point[axis_from] < cutoff and cmp_is_below:
        new_point[axis_to] += sign * (cutoff - point[axis_from])
        new_point[axis_from] = cutoff
    elif point[axis_from] > cutoff and not cmp_is_below:
        new_point[axis_to] += sign * (point[axis_from] - cutoff)
        new_point[axis_from] = cutoff
        # print("rock {} -> {}".format(point, new_point))
    return tuple(new_point)

def fold(cutoff, axis_from, axis_to, cmp_is_below, fold_negative, rocks, faces):
    new_rocks = dict()
    new_faces = set()
    sign = 1
    if fold_negative:
        sign = -1
    axis_to_set = set()
    for r in rocks:
        new_r = list(r)
        if r[axis_from] < cutoff and cmp_is_below:
            axis_to_set.add(r[axis_to])
            new_r[axis_to] += sign * (cutoff - r[axis_from])
            new_r[axis_from] = cutoff
        elif r[axis_from] > cutoff and not cmp_is_below:
            axis_to_set.add(r[axis_to])
            new_r[axis_to] += sign * (r[axis_from] - cutoff)
            new_r[axis_from] = cutoff
            # print("rock {} -> {}".format(r, new_r))
        new_rocks[tuple(new_r)] = rocks[r]
    if len(axis_to_set) > 1:
        # We are not folding a plane like we envisioned.
        print(cutoff, axis_from, axis_to, cmp_is_below, fold_negative)
        raise ValueError()
    for r in faces:
        new_r = list(r)
        if r[axis_from] < cutoff and cmp_is_below:
            new_r[axis_to] += sign * (cutoff - r[axis_from])
            new_r[axis_from] = cutoff
        elif r[axis_from] > cutoff and not cmp_is_below:
            new_r[axis_to] += sign * (r[axis_from] - cutoff)
            new_r[axis_from] = cutoff
            # print("face: {} -> {}".format(r, new_r))
        new_faces.add(tuple(new_r))
    return new_rocks, new_faces

def print_rocks(rocks, player=None):
    minx = min([r[0] for r in rocks])
    maxx = max([r[0] for r in rocks])
    miny = min([r[1] for r in rocks])
    maxy = max([r[1] for r in rocks])
    minz = min([r[2] for r in rocks])
    maxz = max([r[2] for r in rocks])
    print("({}-{}, {}-{}, {}-{})".format(minx, maxx, miny, maxy, minz, maxz))
    for z in range(minz, maxz + 1):
        print("Z:", z)
        for y in range(miny, maxy + 1):
            for x in range(minx, maxx + 1):
                if player != None:
                    if (x,y,z) == tuple(player):
                        print('X', end='')
                        continue
                if (x,y,z) in rocks:
                    print(rocks[x,y,z].char, end='')
                else:
                    print(' ', end='')
            print()

def settle_point(p, rocks):
    point = list(p)
    while True:
        if (point[0] - 1, point[1], point[2]) in rocks:
            point[0] -= 1
            continue
        if (point[0], point[1] - 1, point[2]) in rocks:
            point[1] -= 1
            continue
        if (point[0], point[1], point[2] - 1) in rocks:
            point[2] -= 1
            continue
        break
    return tuple(point)

def get_fold_args(corner, rocks, length):
    x = corner[0]
    y = corner[1]
    z = corner[2]
    if x == 6 and y == 1 and z == 3:
        print(1)
    point = None
    if (x - 2, y, z) in rocks:
        cutoff = x - 1
        axis_from = 0
        if (x - 2, y + 1, z) in rocks:
            axis_to = 2
        else:
            axis_to = 1
        cmp_is_below = True
        point = (x - length - 1, y, z)
    elif (x + length + 1, y, z) in rocks and (x + 1, y, z) in rocks:
        cutoff = x + length
        axis_from = 0
        if (x + length + 1, y + 1, z) in rocks:
            axis_to = 2
        else:
            axis_to = 1
        cmp_is_below = False
        point = (x + length + 1, y, z)
    elif (x, y - 2, z) in rocks:
        cutoff = y - 1
        axis_from = 1
        if (x + 1, y - 2, z) in rocks:
            axis_to = 2
        else:
            axis_to = 0
        cmp_is_below = True
        point = (x, y - length - 1, z)
    elif (x, y + length + 1, z) in rocks and (x, y + 1, z) in rocks:
        cutoff = y + length
        axis_from = 1
        if (x + 1, y + length + 1, z) in rocks:
            axis_to = 2
        else:
            axis_to = 0
        cmp_is_below = False
        point = (x, y + length + 1, z)

    elif (x, y, z - 2) in rocks:
        cutoff = z - 1
        axis_from = 2
        if (x + 1, y, z - 2) in rocks:
            axis_to = 1
        else:
            axis_to = 0
        cmp_is_below = True
        point = (x, y, z - length - 1)

    elif (x, y, z + length + 1) in rocks and (x, y, z + 1) in rocks:
        cutoff = z + length
        axis_from = 2
        if (x + 1, y, z + length + 1) in rocks:
            axis_to = 1
        else:
            axis_to = 0
        cmp_is_below = False
        point = (x, y, z + length + 1)
    if point == None:
        return None, None, None, None, None
    return cutoff, axis_from, axis_to, cmp_is_below, point

def fold_cube(beginning, baseline, rocks, faces, length):
    if (beginning == (3,1,3)):
        print(1)
    new_points = []
    while True:
        cutoff, axis_from, axis_to, cmp_is_below, point = get_fold_args(beginning, rocks, length)
        if point == None:
            break
        fold_negative = False
        if baseline[axis_to] < point[axis_to]:
            fold_negative = True
        rocks, faces = fold(cutoff, axis_from, axis_to, cmp_is_below, fold_negative, rocks, faces)
        new_points.append(fold_point(cutoff, axis_from, axis_to, cmp_is_below, fold_negative, point))

    for p in new_points:
        p = settle_point(p, rocks)
        rocks, faces = fold_cube(p, baseline, rocks, faces, length)
    return rocks, faces

def get_adjacent_edge_cube(tile, rocks_cube, rocks_2d):
    adjacent = [] # ((enter_direction, enter_coords), (exit_direction, exit_coords)
    directions = {(0,1):'R', (1,0):'D', (0,-1):'L', (-1,0):'U'}
    normal = 2
    cube_coords = tile.cube_coords
    if ((cube_coords[0] + 1, cube_coords[1], cube_coords[2]) not in rocks_cube and
        (cube_coords[0] - 1, cube_coords[1], cube_coords[2]) not in rocks_cube):
        normal = 0
    elif ((cube_coords[0], cube_coords[1] + 1, cube_coords[2]) not in rocks_cube and
          (cube_coords[0], cube_coords[1] - 1, cube_coords[2]) not in rocks_cube):
        normal = 1
    for vector in directions:
        enter_direction = directions[vector]
        if ((tile.coords[0] - vector[0], tile.coords[1] - vector[1]) in rocks_2d and
            (tile.coords[0] + vector[0], tile.coords[1] + vector[1]) not in rocks_2d):
            enter_coords = (tile.coords[0] + vector[0], tile.coords[1] + vector[1])
            adj_cube_coords = rocks_2d[(tile.coords[0] - vector[0], tile.coords[1] - vector[1])].cube_coords
            vector3d = []
            check_coords = []
            for i in range(3):
                vector3d.append(cube_coords[i] - adj_cube_coords[i])
                check_coords.append(cube_coords[i] + vector3d[i])
            
            for sign in (1, -1):
                check_coords[normal] += sign
                # Get the exiting direction.
                if tuple(check_coords) in rocks_cube:
                    exit_coords = rocks_cube[tuple(check_coords)].coords
                    t1 = rocks_cube[tuple(check_coords)]
                    check_coords[normal] += sign
                    t2 = rocks_cube[tuple(check_coords)]
                    check_coords[normal] -= sign
                    vector2d = (t2.coords[0] - t1.coords[0], t2.coords[1] - t1.coords[1])
                    exit_direction = directions[vector2d]
                    adjacent.append(((enter_direction, enter_coords), (exit_direction, exit_coords)))
                check_coords[normal] -= sign
    return adjacent
    

def part2(arr):
    length = estimate_cube_length(arr)
    rocks_cube = dict() # (x, y, z) : Tile object
    rocks_2d = dict() # (x, y) : tile object
    faces = set() # (x, y, z)
    beginning = None
    beginning_tile = None

    row_offset = 0
    row = 0
    while True:
        line = arr[row]
        if line == '':
            row += 1
            break
        col = 0
        col_offset = 0
        while col < len(line):
            if line[col] != ' ':
                face_added = False
                for r in range(length):
                    for c in range(length):
                        rock_tile = Tile(arr[row + r][col + c], (row + r + 1, col + c + 1))
                        if not face_added:
                            faces.add((col + c, row + r, 0))
                            face_added = True
                        if beginning == None:
                            beginning = (col + c + col_offset, row + r + row_offset, 0)
                            beginning_tile = rock_tile
                        rocks_cube[(col + c + col_offset, row + r + row_offset, 0)] = rock_tile
                        rocks_2d[(row + r + 1, col + c + 1)] = rock_tile
            col += length
            col_offset += 1
        row += length
        row_offset += 1
    instructions = arr[row]

    rocks_cube, faces = fold_cube(beginning, beginning, rocks_cube, faces, length)
    for rock in rocks_cube:
        rocks_cube[rock].cube_coords = rock

    teleporters = dict() # (face, 2d coords):(face, 2d coords) 
    tiles = [beginning_tile]
    visited = set() # 2d Coords
    directions = {'R':(0,1), 'D':(1,0), 'L':(0,-1), 'U':(-1,0)}
    while len(tiles) > 0:
        curr_tile = tiles.pop()
        curr_coords = curr_tile.coords
        for face in directions:
            vector = directions[face]
            next_coords = (curr_coords[0] + vector[0], curr_coords[1] + vector[1])
            if next_coords in visited:
                continue
            if next_coords not in rocks_2d:
                teleport_tiles = get_adjacent_edge_cube(curr_tile, rocks_cube, rocks_2d)
                for tp in teleport_tiles:
                    teleporters[tp[0]] = tp[1]
            else:
                tiles.append(rocks_2d[next_coords])
                visited.add(next_coords)

    player_coords = list(beginning_tile.coords)
    player_direction = 'R'
    player_direction_i = 0
    direction_cycle = ['R', 'D', 'L', 'U']
    i = 0
    steps = 0
    while i <= len(instructions):
        if (i != len(instructions) and instructions[i].isnumeric()):
            steps *= 10
            steps += int(instructions[i])
        else:
            while steps > 0:
                vector = directions[player_direction]
                new_position = (player_coords[0] + vector[0], player_coords[1] + vector[1])
                if (new_position not in rocks_2d):
                    tp_dest = teleporters[(player_direction, new_position)]
                    new_position = tp_dest[1]
                    if (rocks_2d[new_position].char == '.'):
                        player_direction = tp_dest[0]
                        player_direction_i = direction_cycle.index(player_direction)
                    else:
                        break
                if (rocks_2d[new_position].char == '.'):
                    player_coords[0] = new_position[0]
                    player_coords[1] = new_position[1]
                else:
                    break
                steps -= 1
            steps = 0
            if i != len(instructions):
                if (instructions[i] == 'R'):
                    player_direction_i = (player_direction_i + 1) % len(direction_cycle)
                elif (instructions[i] == 'L'):
                    player_direction_i = (player_direction_i - 1) % len(direction_cycle)
                else:
                    raise ValueError()
            player_direction = direction_cycle[player_direction_i]
        i += 1
    print("Part 2:", 1000*(player_coords[0]) + 4*(player_coords[1]) + player_direction_i)
    return

def play_part2(beginning_coords, rocks_2d, teleporters):
    directions = {'R':(0,1), 'D':(1,0), 'L':(0,-1), 'U':(-1,0)}
    player_direction = 'R'
    player_coords = list(beginning_coords)
    while True:
        gridmap = ""
        for row, line in enumerate(arr):
            if line == '':
                break
            for col, char in enumerate(line):
                if [row + 1, col + 1] == player_coords:
                    gridmap += 'X'
                else:
                    gridmap += char
            gridmap += '\n'
        print(gridmap)
        d = input()
        if d == 'w':
            new_coords = (player_coords[0] + directions['U'][0], player_coords[1] + directions['U'][1])
            player_direction = 'U'
        elif d == 's':
            new_coords = (player_coords[0] + directions['D'][0], player_coords[1] + directions['D'][1])
            player_direction = 'D'
        elif d == 'd':
            new_coords = (player_coords[0] + directions['R'][0], player_coords[1] + directions['R'][1])
            player_direction = 'R'
        elif d == 'a':
            new_coords = (player_coords[0] + directions['L'][0], player_coords[1] + directions['L'][1])
            player_direction = 'L'
        else:
            new_coords = (player_coords[0], player_coords[1])
        if (player_direction, new_coords) in teleporters:
            new_coords = teleporters[(player_direction, new_coords)][1]
            if rocks_2d[new_coords].char == '#':
                continue
        if new_coords in rocks_2d:
            if rocks_2d[new_coords].char == '#':
                continue
            else:
                player_coords[0] = new_coords[0]
                player_coords[1] = new_coords[1]

def part1(arr):
    
    col_lens = defaultdict(int)
    col_start = dict()
    row_lens = defaultdict(int)
    row_start = defaultdict(int)
    grid = dict()
    i = 0
    for i, line in enumerate(arr):
        if line == '':
            i += 1
            break
        for col, char in enumerate(line):
            if char == ' ':
                row_start[i] += 1
                continue
            else:
                grid[(i, col)] = char
                col_lens[col] += 1
                row_lens[i] += 1
                if (col not in col_start):
                    col_start[col] = i


    directions = {'R':(0,1), 'D':(1,0), 'L':(0,-1), 'U':(-1,0)}
    player_r = 0
    player_c = row_start[0]
    player_direction_i = 0
    player_direction = 'R'
    direction_cycle = ['R', 'D', 'L', 'U']
    instructions = arr[i]

    i = 0
    steps = 0
    while i <= len(instructions):
        if (i != len(instructions) and instructions[i].isnumeric()):
            steps *= 10
            steps += int(instructions[i])
        else:
            vector = directions[player_direction]
            while steps > 0:
                new_position = (player_r + vector[0], player_c + vector[1])
                if (new_position not in grid):
                    if player_direction == 'R':
                        new_position = (player_r, player_c - row_lens[player_r] + 1)
                    elif player_direction == 'L':
                        new_position = (player_r, player_c + row_lens[player_r] - 1)
                    elif player_direction == 'U':
                        new_position = (player_r + col_lens[player_c] - 1, player_c)
                    elif player_direction == 'D':
                        new_position = (player_r - col_lens[player_c] + 1, player_c)
                    else:
                        raise ValueError()
                if (grid[new_position] == '.'):
                    player_r = new_position[0]
                    player_c = new_position[1]
                else:
                    break
                steps -= 1
            steps = 0
            if i != len(instructions):
                if (instructions[i] == 'R'):
                    player_direction_i = (player_direction_i + 1) % len(direction_cycle)
                elif (instructions[i] == 'L'):
                    player_direction_i = (player_direction_i - 1) % len(direction_cycle)
                else:
                    raise ValueError()
            player_direction = direction_cycle[player_direction_i]
        i += 1
    print("Part 1:", 1000*(player_r + 1) + 4*(player_c + 1) + player_direction_i)


def solve(arr):
    part1(arr)
    part2(arr)

if __name__ == '__main__':
    filename = "input22.txt"
    arr = arrayise(filename)
    solve(arr)
    