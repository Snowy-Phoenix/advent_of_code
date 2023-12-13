import math
import re
import numpy as np
import itertools
import time
from collections import deque

class Tile:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def get_moves(self):
        raise NotImplementedError
    def get_type(self):
        raise NotImplementedError
class Wall(Tile):
    def get_moves(self):
        return []
    def get_type(self):
        return 'w'
    def __repr__(self):
        return '#'
    
    
class Air(Tile):
    def get_moves(self):
        return [Coordinate(self.row + 1, self.col), 
                Coordinate(self.row, self.col + 1), 
                Coordinate(self.row - 1, self.col), 
                Coordinate(self.row, self.col - 1)]
    def get_type(self):
        return 'a'
    def __repr__(self):
        return '.'
class Teleporter(Tile):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.teleport_link = None
        self.is_inner = False
    def get_moves(self):
        moves = [Coordinate(self.row + 1, self.col), 
                 Coordinate(self.row, self.col + 1), 
                 Coordinate(self.row - 1, self.col), 
                 Coordinate(self.row, self.col - 1)]
        if self.teleport_link is not None:
            moves.append(self.teleport_link)
        return moves
    def get_type(self):
        return 't'
    def __repr__(self):
        return '@'
    def link(self, row, col):
        layer_change = 0
        if self.is_inner:
            layer_change = 1
        else:
            layer_change = -1
        self.teleport_link = Coordinate(row, col, layer_change)
        
    def set_is_inner(self, is_inner):
        self.is_inner = is_inner
class Coordinate:
    def __init__(self, row, col, layer_change=0):
        self.row = row
        self.col = col
        self.layer_change = layer_change
    def __hash__(self):
        return hash((self.row, self.col))
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    def __repr__(self):
        return str((self.row, self.col))
class Maze:
    def __init__(self, maze_array):
        self.maze = np.zeros([len(maze_array), len(maze_array[0])], dtype=np.object)
        self.beginning = None
        self.end = None
        self.parse_maze(maze_array)
    
    def parse_maze(self, maze_array):
        teleporters_unlinked = dict() # Letter, teleporter object
        for r, row in enumerate(maze_array):
            for c, tile in enumerate(row):
                if self.maze[r][c] != 0:
                    continue
                if tile == '.' or tile == ' ':
                    self.maze[r][c] = Air(r, c)
                elif tile == '#':
                    self.maze[r][c] = Wall(r, c)
                elif tile.isalpha():
                    letter, teleporter, walls = self.parse_teleporter(maze_array, r, c)
                    if letter == None:
                        self.maze[r][c] = Wall(r, c)
                        continue
                    if letter == 'AA':
                        self.beginning = Coordinate(teleporter.row, teleporter.col)
                        teleporter = Air(teleporter.row, teleporter.col)
                    elif letter == 'ZZ':
                        self.end = Coordinate(teleporter.row, teleporter.col)
                        teleporter = Air(teleporter.row, teleporter.col)
                    elif letter in teleporters_unlinked:
                        other = teleporters_unlinked.pop(letter)
                        if teleporter.row == 2 or teleporter.col == 2:
                            teleporter.set_is_inner(False)
                            other.set_is_inner(True)
                        elif teleporter.row == len(self.maze) - 3 or \
                                teleporter.col == len(self.maze[teleporter.row]) - 3:
                            teleporter.set_is_inner(False)
                            other.set_is_inner(True)
                        else:
                            teleporter.set_is_inner(True)
                            other.set_is_inner(False)
                        teleporter.link(other.row, other.col)
                        other.link(teleporter.row, teleporter.col)
                    else:
                        teleporters_unlinked[letter] = teleporter
                    for wall_r, wall_c in walls:
                        self.maze[wall_r][wall_c] = Wall(wall_r, wall_c)
                    self.maze[teleporter.row][teleporter.col] = teleporter
        if self.beginning is None or self.end is None:
            print("Unable to get start or beginning.")
            exit(1)

    def parse_teleporter(self, maze_array, row, col):
        letter1 = maze_array[row][col]
        letter2 = None
        teleporter = None
        walls = [(row, col)]
        # upwards
        if self.__get_tile(maze_array, row - 1, col).isalpha():
            letter2 = letter1
            letter1 = self.__get_tile(maze_array, row - 1, col)
            if self.__get_tile(maze_array, row - 2, col) == '.':
                teleporter = Teleporter(row - 2, col)
                walls.append((row - 1, col))
        # Rightwards
        elif self.__get_tile(maze_array, row, col + 1).isalpha():
            letter2 = self.__get_tile(maze_array, row, col + 1)
            if self.__get_tile(maze_array, row, col + 2) == '.':
                teleporter = Teleporter(row, col + 2)
                walls.append((row, col + 1))
        # Downwards
        elif self.__get_tile(maze_array, row + 1, col).isalpha():
            letter2 = self.__get_tile(maze_array, row + 1, col)
            if self.__get_tile(maze_array, row + 2, col) == '.':
                teleporter = Teleporter(row + 2, col)
                walls.append((row + 1, col))
        # Leftwards
        elif self.__get_tile(maze_array, row, col - 1).isalpha():
            letter2 = letter1
            letter1 = self.__get_tile(maze_array, row, col - 1)
            if self.__get_tile(maze_array, row, col - 2) == '.':
                teleporter = Teleporter(row, col - 2)
                walls.append((row, col - 1))
        if letter2 == None or teleporter == None:
            return None, None, None
        else:
            return letter1 + letter2, teleporter, walls

    
    def __get_tile(self, maze_array, row, col):
        if -1 < row < len(maze_array):
            if -1 < col < len(maze_array[row]):
                return maze_array[row][col]
        return '#'

    def get_tile_object(self, coordinates):
        return self.maze[coordinates.row][coordinates.col]
    
    def get_start(self):
        return self.beginning
    
    def is_end(self, coordinates, level=0):
        return self.end == coordinates

class BreadthFirstSearch:
    class Node:
        def __init__(self, coords, layer, steps, parent=None):
            self.coords = coords
            self.layer = layer
            self.steps = steps
            self.parent = parent
        def __repr__(self):
            return str((self.coords, self.layer, self.steps))
        def __hash__(self):
            return hash((self.coords, self.layer))
        def __eq__(self, other):
            return self.coords == other.coords and self.layer == other.layer
    def __init__(self, maze):
        self.maze = maze

    def run(self):
        start = self.maze.get_start()
        start_node = self.Node(start, 0, 0)
        queue = deque()
        queue.append(start_node)
        visited = set()
        while len(queue) > 0:
            curr_node = queue.popleft()
            curr_coords = curr_node.coords
            curr_steps = curr_node.steps
            if curr_coords in visited:
                continue
            if self.maze.is_end(curr_coords):
                print("Part 1:", curr_steps)
                break
            visited.add(curr_coords)
            curr_tile = self.maze.get_tile_object(curr_coords)
            moves = curr_tile.get_moves()
            for move in moves:
                if move not in visited:
                    queue.append(self.Node(move, 0, curr_steps + 1))
        

    def run_recursive(self):
        start = self.maze.get_start()
        start_node = self.Node(start, 0, 0)
        queue = deque()
        queue.append(start_node)
        visited = set()
        while len(queue) > 0:
            curr_node = queue.popleft()
            curr_coords = curr_node.coords
            curr_steps = curr_node.steps
            curr_layer = curr_node.layer
            if curr_node in visited:
                continue
            if curr_node.layer == 0 and self.maze.is_end(curr_coords):
                print("Part 2:", curr_steps)
                break
            visited.add(curr_node)
            curr_tile = self.maze.get_tile_object(curr_coords)
            moves = curr_tile.get_moves()
            for move in moves:
                layer_change = move.layer_change
                new_layer = curr_layer + layer_change
                if new_layer < 0:
                    continue
                new_node = self.Node(move, new_layer, curr_steps + 1)
                if new_node not in visited:
                    queue.append(new_node)

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip('\n'))
    f.close()
    return array

def day20(array):
    maze = Maze(array)
    bfs = BreadthFirstSearch(maze)
    bfs.run()
    bfs.run_recursive()


if __name__ == "__main__":
    filename = "input20.txt"
    arr = arrayise(filename)
    day20(arr)

