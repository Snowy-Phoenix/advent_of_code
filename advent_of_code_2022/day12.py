from collections import deque
from collections import defaultdict

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def solve_first(array):
    grid = []
    startr = 0
    startc = 0
    endr = 0
    endc = 0
    for row, line in enumerate(array):
        grid.append([])
        for col, char in enumerate(line):
            if char == 'S':
                startr = row
                startc = col
                grid[-1].append(0)
            elif char == 'E':
                endr = row
                endc = col
                grid[-1].append(25)
            else:
                grid[-1].append(ord(char) - ord('a'))
    visited = set()
    fringe = deque()
    fringe.append((startr, startc, 0))
    visited.add((startr, startc))
    curr_depth = 0
    while len(fringe) > 0:
        tile = fringe.popleft()
        if tile in visited:
            continue
        r = tile[0]
        c = tile[1]
        depth = tile[2]
        if depth > curr_depth:
            curr_depth = depth
        height = grid[r][c]
        if r == endr and c == endc:
            print("Part 1:", depth)
            break
        if r - 1 >= 0:
            if (r-1, c) not in visited:
                h = grid[r-1][c]
                if h <= height + 1:
                    fringe.append((r-1,c,depth + 1))
                    visited.add((r-1,c))
        if c - 1 >= 0:
            if (r, c-1) not in visited:
                h = grid[r][c-1]
                if h <= height + 1:
                    fringe.append((r,c-1,depth + 1))
                    visited.add((r,c-1))
                    
        if c + 1 < len(grid[r]):
            if (r, c+1) not in visited:
                h = grid[r][c+1]
                if h <= height + 1:
                    fringe.append((r,c+1,depth + 1))
                    visited.add((r,c+1))
        if r + 1 < len(grid):
            if (r+1, c) not in visited:
                h = grid[r+1][c]
                if h <= height + 1:
                    fringe.append((r+1,c,depth + 1))
                    visited.add((r+1,c))
    
    shortest = 100000000
    for startr, row in enumerate(grid):
        for startc, starth in enumerate(row):
            
            if starth == 0:
                visited = set()
                fringe = deque()
                fringe.append((startr, startc, 0))
                visited.add((startr, startc))
                curr_depth = 0
                while len(fringe) > 0:
                    tile = fringe.popleft()
                    if tile in visited:
                        continue
                    r = tile[0]
                    c = tile[1]
                    depth = tile[2]
                    if depth > curr_depth:
                        curr_depth = depth
                    height = grid[r][c]
                    if r == endr and c == endc:
                        shortest = min(shortest, depth)
                        break
                    if r - 1 >= 0:
                        if (r-1, c) not in visited:
                            h = grid[r-1][c]
                            if h <= height + 1:
                                fringe.append((r-1,c,depth + 1))
                                visited.add((r-1,c))
                    if c - 1 >= 0:
                        if (r, c-1) not in visited:
                            h = grid[r][c-1]
                            if h <= height + 1:
                                fringe.append((r,c-1,depth + 1))
                                visited.add((r,c-1))
                                
                    if c + 1 < len(grid[r]):
                        if (r, c+1) not in visited:
                            h = grid[r][c+1]
                            if h <= height + 1:
                                fringe.append((r,c+1,depth + 1))
                                visited.add((r,c+1))
                    if r + 1 < len(grid):
                        if (r+1, c) not in visited:
                            h = grid[r+1][c]
                            if h <= height + 1:
                                fringe.append((r+1,c,depth + 1))
                                visited.add((r+1,c))
    print(shortest)

class Grid:
    def __init__(self, grid, rows, cols, endi):
        self.grid = grid
        self.rows = rows
        self.cols = cols
        self.endi = endi
    
    def parse_grid(array):
        grid = []
        rows = 0
        cols = 0
        starti = 0
        endi = 0
        for row, line in enumerate(array):
            for col, char in enumerate(line):
                if (cols == 0):
                    cols = len(line)
                else:
                    assert cols == len(line), "Tile map is not rectangular"
                if char == 'S':
                    starti = row * cols + col
                    grid.append(0)
                elif char == 'E':
                    endi = row * cols + col
                    grid.append(25)
                else:
                    grid.append(ord(char) - ord('a'))
            rows += 1
        return Grid(grid, rows, cols, endi), starti

    def get_valid_moves(self, index, reverse=False):
        valid_moves = []
        moves = [-self.cols, 1, self.cols, -1] # Up, right, down, left
        grid_len = self.rows * self.cols
        for move in moves:
            potential_move = index + move
            if 0 <= index + move < grid_len:
                if ((index // self.cols == potential_move // self.cols) or 
                    (abs(potential_move - index) == self.cols)):
                    curr_h = self.grid[index]
                    next_h = self.grid[potential_move]
                    if (next_h <= curr_h + 1) and not reverse:
                        valid_moves.append((index + move))
                    elif (curr_h <= next_h + 1) and reverse:
                        valid_moves.append((index + move))
        return valid_moves

    def get_tile(self, index):
        return self.grid[index]
    def is_end(self, index, reverse=False):
        if reverse:
            return self.grid[index] == 0
        return self.endi == index

def get_shortest_path(grid, starti, reverse=False):
    visited = set()
    fringe = deque()
    fringe.append((starti, 0)) # Coordinates, depth
    visited.add(starti)
    while len(fringe) > 0:
        tile = fringe.popleft()
        index = tile[0]
        depth = tile[1]
        valid_moves = grid.get_valid_moves(index, reverse)
        for move in valid_moves:
            if grid.is_end(move, reverse):
                return depth + 1
            else:
                if move not in visited:
                    visited.add(move)
                    fringe.append((move, depth + 1))

def solve(array):
    grid, starti = Grid.parse_grid(array)
    print("Part 1:", get_shortest_path(grid, starti))
    print("Part 2:", get_shortest_path(grid, grid.endi, reverse=True))

if __name__ == '__main__':
    filename = "input12.txt"
    arr = arrayise(filename)
    # solve_first(arr)
    solve(arr)
