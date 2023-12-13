import heapq
import math
import re
import numpy as np
import itertools
from intcode import IntcodeInterpreter
from collections import deque


class TileMap:
    def __init__(self):
        self.map = []
        self.coord_keys = dict()  # coords, key_value
        self.key_coords = dict()  # key_value, coords
        self.doors = dict()       # coords, door_value
        self.start_pos = 0
        self.rows = 0
        self.cols = 0
        self.get_moves_cache = dict()  # (start, keyset), [moves]

    def fill_sectors(self):
        filled_map = np.zeros(len(self.map), dtype=np.str)
        quadrant = 0
        for i, t in enumerate(self.map):
            if filled_map[i] == '':
                if t == '.':
                    if i in self.doors:
                        filled_map[i] = self.doors[i]
                        continue
                    quadrant += 1
                    visited = set()
                    stack = deque()
                    stack.append(i)
                    moves = [-self.cols, 1, self.cols, -1]
                    while len(stack) > 0:
                        curr_i = stack.pop()
                        visited.add(curr_i)
                        filled_map[curr_i] = str(quadrant)
                        for move in moves:
                            new_coords = curr_i + move
                            if new_coords in visited:
                                continue
                            if self.is_legal(new_coords, []):
                                stack.append(new_coords)
                else:
                    filled_map[i] = t
            if i in self.coord_keys:
                filled_map[i] = self.coord_keys[i]
        np.savetxt("maze.txt", np.reshape(
            filled_map, [self.rows, self.cols]), fmt='%s', delimiter='')
        print(np.reshape(filled_map, [self.rows, self.cols]))

    def generate_map(self, tiles):
        self.rows = len(tiles)
        self.cols = len(tiles[0])
        for r, tile_row in enumerate(tiles):
            for c, tile in enumerate(tile_row):
                if tile == '@':
                    self.start_pos = r * self.cols + c
                    self.map.append('.')
                elif tile.isalpha():
                    if tile.isupper():
                        self.doors[r * self.cols + c] = tile
                    else:
                        self.coord_keys[r * self.cols + c] = tile
                        self.key_coords[tile] = r * self.cols + c
                    self.map.append('.')
                elif tile == '.':
                    self.map.append('.')
                else:
                    self.map.append('#')
        self.map = np.array(self.map)

    def is_legal(self, position, collected_keys):
        if self.map[position] == '#':
            return False
        elif position in self.doors:
            if self.doors[position].lower() not in collected_keys:
                return False
        return True

    def get_moves(self, start=-1, collected_keys=set()):
        if (start, tuple(sorted(collected_keys))) in self.get_moves_cache:
            return self.get_moves_cache[(start, tuple(sorted(collected_keys)))]
        if start == -1:
            start = self.start_pos
        moves = [-self.cols, 1, self.cols, -1]  # up, right, down, left
        visited = set()
        queue = deque()
        queue.append((start, 0))
        possible_moves = []  # (position, steps)
        while len(queue) > 0:
            position, steps = queue.popleft()
            visited.add(position)
            if position in self.coord_keys:
                if self.coord_keys[position] not in collected_keys:
                    possible_moves.append((position, steps))
                    continue
            for move in moves:
                new_position = position + move
                if new_position in visited:
                    continue
                if self.is_legal(new_position, collected_keys):
                    queue.append((new_position, steps + 1))
        self.get_moves_cache[(start, tuple(
            sorted(collected_keys)))] = possible_moves
        return possible_moves

    def get_key(self, coords):
        if coords in self.coord_keys:
            return self.coord_keys[coords]
        return ''
    
    def remove_dead_ends(self):
        moves = [-self.cols, 1, self.cols, -1] # up, right, down, left
        tile_map = np.copy(self.map)
        for i in self.coord_keys:
            tile_map[i] = self.coord_keys[i]
        for i in self.doors:
            tile_map[i] = self.doors[i]
        changed = True
        while changed:
            changed = False
            for i, t, in enumerate(tile_map):
                if t == '#':
                    continue
                if t.islower():
                    continue
                walls = 0
                for move in moves:
                    if tile_map[i + move] == '#':
                        walls += 1
                if walls >= 3:
                    tile_map[i] = '#'
                    changed = True
        tile_map[self.start_pos] = '@'
        np.savetxt("tilemap.txt", np.reshape(tile_map, [self.rows, self.cols]), fmt='%s', delimiter='')
        new_map = TileMap()
        new_map.generate_map(np.reshape(tile_map, [self.rows, self.cols]))
        return new_map


class Node:
    def __init__(self, keys, steps, current_key):
        self.keys = set(keys)
        self.steps = steps
        self.current_key = current_key

    def __hash__(self):
        return hash((tuple(sorted(self.keys)), self.current_key))

    def __eq__(self, other):
        return self.keys == other.keys and self.current_key == other.current_key

    def __lt__(self, other):
        return self.steps < other.steps

    def __gt__(self, other):
        return self.steps > other.steps

    def __le__(self, other):
        return self.steps <= other.steps

    def __ge__(self, other):
        return self.steps >= other.steps


class UniformCostSearch:
    def __init__(self):
        self.visited = set()
        self.pq = []
        self.tile_map = TileMap()

    def is_goal(self, node):
        return node.keys == set(self.tile_map.key_coords.keys())

    def initialise_search(self, tile_map):
        self.tile_map.generate_map(tile_map)
        self.tile_map = self.tile_map.remove_dead_ends()
        moves = self.tile_map.get_moves()
        for move in moves:
            coords, steps = move
            new_key = self.tile_map.get_key(coords)
            heapq.heappush(self.pq, Node([new_key], steps, new_key))

    def run(self, tile_map):
        self.initialise_search(tile_map)
        while len(self.pq) > 0:
            curr_node = heapq.heappop(self.pq)
            if curr_node in self.visited:
                continue
            if self.is_goal(curr_node):
                return curr_node.steps
            self.visited.add(curr_node)

            start = self.tile_map.key_coords[curr_node.current_key]
            collected_keys = curr_node.keys
            possible_moves = self.tile_map.get_moves(start, collected_keys)
            for move in possible_moves:
                coords, steps = move
                new_curr_key = self.tile_map.get_key(coords)
                new_keys = curr_node.keys.union([new_curr_key])
                new_steps = curr_node.steps + steps
                new_node = Node(new_keys, new_steps, new_curr_key)
                if new_node in self.visited:
                    continue
                else:
                    heapq.heappush(self.pq, new_node)


def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array


def day18a(array):
    searcher = UniformCostSearch()
    print(searcher.run(array))


if __name__ == "__main__":
    filename = "input18.txt"
    arr = arrayise(filename)
    day18a(arr)
