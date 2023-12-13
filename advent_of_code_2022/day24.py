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

class Node:
    def __init__(self, coords, blizzard_state, turns, heuristic_function, state=-1):
        self.coords = coords
        self.blizzard_state = blizzard_state
        self.turns = turns
        self.heuristic_function = heuristic_function
        self.state = state
        self.heuristic = 0
        if self.state == -1:
            self.heuristic = turns + heuristic_function(coords)
        else:
            self.heuristic = turns + heuristic_function(coords, state)
    
    def __lt__(self, other):
        return self.heuristic < other.heuristic
    def __repr__(self):
        return str((self.coords, self.blizzard_state, self.turns, self.heuristic))

def print_grid(blizzards, nrows, ncols, start, end, player_coords):
    print(player_coords)
    for r in range(nrows):
        for c in range(ncols):
            if player_coords != None:
                if r == player_coords[0] and c == player_coords[1]:
                    print("E", end='')
                    continue
            if r == 0 and c == start:
                print(".", end='')
            elif r == nrows - 1 and c == end:
                print(".", end='')
            elif r == 0 or c == 0 or r == nrows - 1 or c == ncols - 1:
                print("#", end='')
            elif (r, c) in blizzards:
                if len(blizzards[(r,c)]) > 1:
                    print(len(blizzards[(r,c)]), end='')
                else:
                    print(blizzards[(r,c)][0], end='')
            else:
                print(".", end='')
        print()
    print()

def simulate(blizzards, num_rows, num_cols):
    new_blizzards = defaultdict(list)
    for coords in blizzards:
        for b in blizzards[coords]:
            row = coords[0]
            col = coords[1]
            if b == '^':
                row -= 1
            elif b == '>':
                col += 1
            elif b == 'v':
                row += 1
            elif b == '<':
                col -= 1
            if row == 0:
                row = num_rows - 2
            elif row == num_rows - 1:
                row = 1
            if col == 0:
                col = num_cols - 2
            if col == num_cols - 1:
                col = 1
            new_blizzards[(row, col)].append(b)
    return new_blizzards

def part1(blizzard_states, num_rows, num_cols, start, end, heuristic_function):
    start_col = start[1]
    end_col = end[1]
    total_states = len(blizzard_states)
    end_coords = (num_rows - 1, end_col)
    moves = []
    moves.append(Node((0, start_col), 0, 0, heuristic_function))
    visited = set() # (Coordinates, blizzard_state)
    visited.add(((0, start_col), 0))
    move_vectors = ((0,0), (0,1), (0,-1), (1,0), (-1,0))
    while len(moves) > 0:
        curr_node = heapq.heappop(moves)
        if curr_node.coords[0] == end_coords[0] and curr_node.coords[1] == end_coords[1]:
            print("Part 1:", curr_node.turns)
            return
        next_blizzard_state = blizzard_states[(curr_node.blizzard_state + 1) % total_states]
        # print_grid(current_blizzard_state, num_rows, num_cols, start_col, end_col, m)
        for vector in move_vectors:
            next_move = (curr_node.coords[0] + vector[0], curr_node.coords[1] + vector[1])
            if next_move in next_blizzard_state:
                continue
            elif (next_move, (curr_node.turns + 1) % total_states) in visited:
                 continue
            elif next_move[0] == 0 and next_move[1] == start_col:
                pass
            elif next_move[0] == num_rows - 1 and next_move[1] == end_col:
                pass
            elif next_move[0] <= 0 or next_move[0] >= num_rows - 1:
                continue
            elif next_move[1] <= 0 or next_move[1] >= num_cols - 1:
                continue
            heapq.heappush(moves, Node(next_move, (curr_node.blizzard_state + 1) % total_states, curr_node.turns + 1, heuristic_function))
            visited.add((next_move, (curr_node.turns + 1) % total_states))

def part2(blizzard_states, num_rows, num_cols, start, end, heuristic_function):
    start_col = start[1]
    end_col = end[1]
    total_states = len(blizzard_states)
    end_coords = (num_rows - 1, end_col)
    moves = []
    moves.append(Node((0, start_col), 0, 0, heuristic_function, 1))
    visited = set() # (Coordinates, blizzard_state, node_state)
    visited.add(((0, start_col), 0, 1))
    move_vectors = ((0,0), (0,1), (0,-1), (1,0), (-1,0))
    while len(moves) > 0:
        curr_node = heapq.heappop(moves)
        next_state = curr_node.state
        if curr_node.coords[0] == end_coords[0] and curr_node.coords[1] == end_coords[1] and curr_node.state == 3:
            print("Part 2:", curr_node.turns)
            return
        elif curr_node.coords[0] == end_coords[0] and curr_node.coords[1] == end_coords[1] and curr_node.state == 1:
            next_state = 2
        elif curr_node.coords[0] == start[0] and curr_node.coords[1] == start[1] and curr_node.state == 2:
            next_state = 3
        next_blizzard_state = blizzard_states[(curr_node.blizzard_state + 1) % total_states]
        # print_grid(current_blizzard_state, num_rows, num_cols, start_col, end_col, m)
        for vector in move_vectors:
            next_move = (curr_node.coords[0] + vector[0], curr_node.coords[1] + vector[1])
            if next_move in next_blizzard_state:
                continue
            elif (next_move, (curr_node.turns + 1) % total_states, next_state) in visited:
                 continue
            elif next_move[0] == 0 and next_move[1] == start_col:
                pass
            elif next_move[0] == num_rows - 1 and next_move[1] == end_col:
                pass
            elif next_move[0] <= 0 or next_move[0] >= num_rows - 1:
                continue
            elif next_move[1] <= 0 or next_move[1] >= num_cols - 1:
                continue
            heapq.heappush(moves, Node(next_move, (curr_node.blizzard_state + 1) % total_states, curr_node.turns + 1, heuristic_function, next_state))
            visited.add((next_move, (curr_node.turns + 1) % total_states, next_state))

def heuristic_part2(coords, state, start, end):
    h = (3 - state)*(abs(end[1] - start[1]) + abs(end[0] - start[0]))
    if state % 2 == 0:
        # Go to the start.
        h += abs(start[0] - coords[0]) + abs(start[1] - coords[1])
    else:
        h += abs(end[0] - coords[0]) + abs(end[1] - coords[1])
    return h

def solve(arr):
    blizzards = defaultdict(list) # (row, col) : list(blizzards)
    start_col = 0
    end_col = 0
    num_rows = len(arr)
    num_cols = len(arr[0])
    row = 0
    for row, line in enumerate(arr):
        if row == 0:
            start_col = line.index(".")
        elif row == len(arr) - 1:
            end_col = line.index(".")
        else:
            for col, char in enumerate(line):
                if char != '.' and char != '#':
                    if (row, col) not in blizzards:
                        blizzards[(row, col)].append(char)
    blizzard_states = dict() # index, state
    blizzard_states[0] = blizzards
    lcm = (num_cols - 2) * (num_rows - 2) // math.gcd(num_rows - 2, num_cols - 2)
    for i in range(1, lcm):
        blizzards = simulate(blizzards, num_rows, num_cols)
        blizzard_states[i] = blizzards
    start = (0, start_col)
    end = (num_rows - 1, end_col)
    heuristic_function1 = lambda coords: abs(end[0] - coords[0]) + abs(end[1] - coords[1])
    heuristic_function2 = lambda coords, state: heuristic_part2(coords, state, start, end)
    part1(blizzard_states, num_rows, num_cols, start, end, heuristic_function1)
    part2(blizzard_states, num_rows, num_cols, start, end, heuristic_function2)

if __name__ == '__main__':
    filename = "input24.txt"
    arr = arrayise(filename)
    solve(arr)
    