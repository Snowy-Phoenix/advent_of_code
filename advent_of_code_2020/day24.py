import re
import numpy as np
import copy

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day24(array):
    # Using (x, y) coordinates
    movement_vectors = {"e":(2,0), "w":(-2,0), "se":(1,-1), "sw":(-1,-1), "ne":(1,1), "nw":(-1, 1)}
    black_tiles = set()
    for line in array:
        move = ""
        i = 0
        x_coord = 0
        y_coord = 0
        while i < len(line):
            move = line[i]
            if move not in movement_vectors:
                i += 1
                move += line[i]
            vector = movement_vectors[move]
            x_coord += vector[0]
            y_coord += vector[1]
            i += 1
        final_coord = (x_coord, y_coord)
        if final_coord in black_tiles:
            black_tiles.remove(final_coord)
        else:
            black_tiles.add(final_coord)
    print("Part 1:", len(black_tiles))

    ticking_white_tiles = dict() # White tile coordinate : number of neighbours
    ticking_black_tiles = dict() # Black tile coordinate : number of neighbours

    for tile in black_tiles:
        ticking_black_tiles[tile] = 0

    for i in range(100):
        for tile in ticking_black_tiles:
            tile_x = tile[0]
            tile_y = tile[1]
            for direction in movement_vectors:
                vector = movement_vectors[direction]
                neighbour_tile_x = tile_x + vector[0]
                neighbour_tile_y = tile_y + vector[1]
                neighbour_tile_coord = (neighbour_tile_x, neighbour_tile_y)
                if neighbour_tile_coord in ticking_black_tiles:
                    ticking_black_tiles[neighbour_tile_coord] += 1
                elif neighbour_tile_coord in ticking_white_tiles:
                    ticking_white_tiles[neighbour_tile_coord] += 1
                else:
                    ticking_white_tiles[neighbour_tile_coord] = 1
        
        for tile in list(ticking_black_tiles.keys()):
            tile_neighbours = ticking_black_tiles[tile]
            if tile_neighbours == 0 or tile_neighbours > 2:
                ticking_black_tiles.pop(tile)
            else:
                ticking_black_tiles[tile] = 0
        
        for tile in ticking_white_tiles:
            tile_neighbours = ticking_white_tiles[tile]
            if tile_neighbours == 2:
                ticking_black_tiles[tile] = 0
        ticking_white_tiles.clear()

    print("Part 2:", len(ticking_black_tiles))
            
if __name__ == "__main__":
    filename = "input24.txt"
    arr = arrayise(filename)
    day24(arr)
