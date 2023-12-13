from collections import deque

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array        

def solve_grid(grid):
    for i in range(1, len(grid)):
        r1 = i - 1
        r2 = i
        equal = True
        diff = 0
        while r1 >= 0 and r2 < len(grid):
            for c in range(len(grid[i])):
                if grid[r1][c] != grid[r2][c]:
                    equal = False
                    break
            r1 -= 1
            r2 += 1
        if equal:
            return 100 * (i)
    
    for i in range(1, len(grid[0])):
        c1 = i - 1
        c2 = i
        equal = True
        while c1 >= 0 and c2 < len(grid[0]):
            for r in range(len(grid)):
                if grid[r][c1] != grid[r][c2]:
                    equal = False
                    break
            c1 -= 1
            c2 += 1
        if equal:
            return i
    return 0

def solve_grid2(grid):
    for i in range(1, len(grid)):
        r1 = i - 1
        r2 = i
        equal = True
        diff = 0
        while r1 >= 0 and r2 < len(grid):
            for c in range(len(grid[i])):
                if grid[r1][c] != grid[r2][c]:
                    equal = False
                    diff += 1
            r1 -= 1
            r2 += 1
        if diff == 1:
            return 100 * (i)
    
    for i in range(1, len(grid[0])):
        c1 = i - 1
        c2 = i
        equal = True
        diff = 0
        while c1 >= 0 and c2 < len(grid[0]):
            for r in range(len(grid)):
                if grid[r][c1] != grid[r][c2]:
                    equal = False
                    diff += 1
            c1 -= 1
            c2 += 1
        if diff == 1:
            return i
    return 0

def solve(arr):
    grid = []
    sums = 0
    s = 0
    for r, line in enumerate(arr):
        if (line == ""):
            sums += solve_grid(grid)
            s += solve_grid2(grid)
            grid = []
            continue
        grid.append([])
        for char in line:
            grid[-1].append(char)
    print(sums + solve_grid(grid))
    print(s + solve_grid2(grid))


if __name__ == '__main__':
    filename = "input13.txt"
    arr = arrayise(filename)
    solve(arr)