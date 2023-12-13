import numpy as np

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day25(array):
    floor_map = []
    for line in array:
        floor_map.append([])
        for c in line:
            floor_map[-1].append(c)
    
    steps = 0
    changed = True
    while changed:
        changed = False
        new_map1 = [[c for c in floor_map[i]] for i in range(len(floor_map))]
        for row in range(len(floor_map)):
            for col in range(len(floor_map[row])):
                tile = floor_map[row][col]
                if tile == '>':
                    next_tile = floor_map[row][(col + 1) % len(floor_map[row])]
                    if next_tile == '.':
                        new_map1[row][col] = '.'
                        new_map1[row][(col + 1) % len(floor_map[row])] = '>'
                        changed = True
        new_map2 = [[c for c in new_map1[i]] for i in range(len(new_map1))]
        for row in range(len(new_map1)):
            for col in range(len(new_map1[row])):
                tile = new_map1[row][col]
                if tile == 'v':
                    next_tile = new_map1[(row + 1) % len(new_map1)][col]
                    if next_tile == '.':
                        new_map2[row][col] = '.'
                        new_map2[(row + 1) % len(new_map1)][col] = 'v'
                        changed = True
        
        steps += 1
        floor_map = new_map2
    print("Part 1:", steps)


if __name__ == "__main__":
    filename = "input25.txt"
    arr = arrayise(filename)
    day25(arr)
