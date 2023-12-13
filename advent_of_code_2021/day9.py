import math
import re

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

class Node:
    def __init__(self, value):
        self.value = value
        self.visited = False

    def __repr__(self):
        return str(self.value)

def day9(arr):
    m = []
    i = 0
    for line in arr:
        m.append([])
        for c in line:
            m[i].append(int(c))
        i += 1
    
    m.insert(0, [9 for i in range(len(m[0]))])
    m.append([9 for i in range(len(m[0]))])
    for i in range(len(m)):
        m[i].insert(0, 9)
        m[i].append(9)


    lowest = []
    coords = set()
    for r in range(1, len(m)-1):
        for c in range(1, len(m[r])-1):
            tile = m[r][c]
            up = m[r - 1][c]
            left = m[r][c - 1]
            down = m[r + 1][c]
            right = m[r][c + 1]
            if tile >= up or tile >= left or tile >= down or tile >= right:
                continue
            else:
                lowest.append(tile)
                coords.add((r, c))
    cumsum = 0
    for i in lowest:
        cumsum += i + 1
    print("Part 1:", cumsum)
    

    for r in range(len(m)):
        for c in range(len(m[r])):
            m[r][c] = Node(m[r][c])
    sizes = []
    for i in coords:
        sizes.append(dfs(m, i[0], i[1]))
    sizes = sorted(sizes)
    print("Part 2:", sizes[-1] * sizes[-2] * sizes[-3])

def dfs(m, r, c):
    up = m[r - 1][c]
    left = m[r][c - 1]
    down = m[r + 1][c]
    right = m[r][c + 1]
    m[r][c].visited = True
    sum = 1
    if not up.visited and up.value != 9:
        sum += dfs(m, r - 1, c)
    if not left.visited and left.value != 9:
        sum += dfs(m, r, c - 1)
    if not down.visited and down.value != 9:
        sum += dfs(m, r + 1, c)
    if not right.visited and right.value != 9:
        sum += dfs(m, r, c + 1)
    return sum


if __name__ == "__main__":
    filename = "input9.txt"
    arr = arrayise(filename)
    day9(arr)

