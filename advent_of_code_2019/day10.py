import math
import re
import numpy as np
import itertools

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

class Asteroid:

    def __init__(self, x, y):
        self.x = x
        self.y = y


    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.x == self.x and other.y == self.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return str((self.x, self.y))

    def __lt__(self, other):
        return math.atan2(self.x, self.y) > math.atan2(other.x, other.y)

def day10(array):
    asteroids = set()
    for y in range(len(array)):
        row = array[y]
        for x in range(len(row)):
            tile = row[x]
            if tile == '#':
                asteroids.add(Asteroid(x, y))
    
    max_y = len(array)
    max_x = len(array[0])
    blocked_tiles = set()
    max_asteroids_seen = 0
    max_base_coords = None
    visible_asteroids_at_max_base = None

    for base_coords in asteroids:
        blocked_tiles = set([base_coords])
        for asteroid in asteroids:
            if asteroid == base_coords:
                continue
            blocked_tiles = blocked_tiles.union(get_blocked_tiles(base_coords, asteroid, max_x, max_y))

        visible_asteroids = asteroids.difference(blocked_tiles)
        asteroids_seen = len(visible_asteroids)
        if asteroids_seen > max_asteroids_seen:
            max_asteroids_seen = asteroids_seen
            max_base_coords = base_coords
            visible_asteroids_at_max_base = visible_asteroids
    
    print("Part 1:", max_base_coords, max_asteroids_seen)

    relative_asteroid_coords = []
    for asteroid in visible_asteroids_at_max_base:
        relative_asteroid_coords.append(Asteroid(asteroid.x - max_base_coords.x , asteroid.y - max_base_coords.y))
    asteroid200 = sorted(relative_asteroid_coords)[199]
    print("Part 2:", 
        (asteroid200.x + max_base_coords.x, asteroid200.y + max_base_coords.y), 
        (asteroid200.x + max_base_coords.x) * 100 + asteroid200.y + max_base_coords.y)


def get_blocked_tiles(base, asteroid, max_x, max_y):
    vector_x = asteroid.x - base.x
    vector_y = asteroid.y - base.y
    common_divisor = math.gcd(vector_x, vector_y)
    vector_x = vector_x // common_divisor
    vector_y = vector_y // common_divisor
    blocked_tiles = set()

    curr_x = vector_x + asteroid.x
    curr_y = vector_y + asteroid.y 
    while 0 <= curr_x < max_x and 0 <= curr_y < max_y:
        blocked_tiles.add(Asteroid(curr_x, curr_y))
        curr_x += vector_x
        curr_y += vector_y
    return blocked_tiles

if __name__ == "__main__":
    filename = "input10.txt"
    arr = arrayise(filename)
    day10(arr)
    

