from collections import deque

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def solve(arr):
    universe = []
    for line in arr:
        universe.append([])
        for c in line:
            universe[-1].append(c)
    
    r = 0
    while r < len(universe):
        line = universe[r]
        is_empty = True        
        for c in line:
            if c == '#':
                is_empty = False
                break
        if (is_empty):
            universe.insert(r, ['|' for _ in universe[r]])
            r += 1
        r += 1
    
    c = 0
    while c < len(universe[0]):
        is_empty = True
        for line in universe:
            if line[c] == '#':
                is_empty = False
                break
        if is_empty:
            for line in universe:
                line.insert(c, "|")
            c += 1
        c += 1
    stars = []

    for r, line in enumerate(universe):
        for c, char in enumerate(line):
            if char == '#':
                stars.append((r, c))
    distances = 0
    for i in range(len(stars)):
        star1 = stars[i]
        for j in range(i + 1, len(stars)):
            star2 = stars[j]
            distances += abs(star1[0]-star2[0]) + abs(star1[1]-star2[1])
    print(distances)

    horizontal_distances = []
    vertical_distances = []
    for i, char in enumerate(universe[0]):
        if char == '|':
            horizontal_distances.append(999999)
        else:
            horizontal_distances.append(1)
    for row in universe:
        if row[0] == "|":
            vertical_distances.append(999999)
        else:
            vertical_distances.append(1)
    
    distances = 0
    for i in range(len(stars)):
        star1 = stars[i]
        for j in range(i + 1, len(stars)):
            star2 = stars[j]
            minx = min(star1[0], star2[0])
            maxx = max(star1[0], star2[0])
            miny = min(star1[1], star2[1])
            maxy = max(star1[1], star2[1])
            distances += sum(horizontal_distances[miny:maxy]) + sum(vertical_distances[minx:maxx])
    print(distances)

if __name__ == '__main__':
    filename = "input11.txt"
    arr = arrayise(filename)
    solve(arr)