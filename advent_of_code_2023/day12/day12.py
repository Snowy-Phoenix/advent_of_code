from collections import deque

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def count_perms(tiles, n, cache):
    if tiles + str(n) in cache:
        return cache[tiles + str(n)]
    count = 0
    if len(n) == 0:
        for char in tiles:
            if char == '#':
                return 0
        return 1
    for i in range(len(tiles)):
        fits = True
        if (i > 0 and tiles[i - 1] == '#'):
            continue
        for j in range(n[0] + 1):
            if i + j >= len(tiles):
                fits = False
                break
            if j == n[0]:
                if not (tiles[i + j] == '?' or tiles[i + j] == '.'):
                    fits = False
                    break
            elif (tiles[i + j] == '?' or tiles[i + j] == '#'):
                continue
            else:
                fits = False
                break
        if (fits):
            count += count_perms(tiles[i + n[0] + 1:], n[1:], cache)
        if tiles[i] == '#':
            break
    cache[tiles + str(n)] = count
    return count
        

def solve(arr):
    combinations = 0
    c2 = 0
    cache = dict()
    for r, line in enumerate(arr):
        tiles, n = line.split()
        n = list(map(int, n.split(',')))
        combinations += count_perms(tiles + '.', n, cache)
        c2 += count_perms(tiles + '?' 
                           + tiles + '?' 
                           + tiles + '?' 
                           + tiles + '?' 
                           + tiles + '?', n + n + n + n + n, cache)
    print(combinations)
    print(c2)

if __name__ == '__main__':
    filename = "input12.txt"
    arr = arrayise(filename)
    solve(arr)