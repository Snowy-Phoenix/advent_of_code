from collections import deque
from collections import defaultdict
import math
import os
import keyboard

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array


class Snake:
    def __init__(self, x, y, length):
        self.length = length
        self.x_segments = [x for _ in range(length)]
        self.y_segments = [y for _ in range(length)]
        self.tail_visited = set()
        self.head_visited = set()

    def propagate(self):
        for i in range(1, self.length):
            if (self.x_segments[i] == self.x_segments[i - 1]
                    or self.y_segments[i] == self.y_segments[i - 1]):
                if (self.x_segments[i] - self.x_segments[i - 1]) > 1:
                    self.x_segments[i] -= 1
                elif self.x_segments[i] - self.x_segments[i - 1] < -1:
                    self.x_segments[i] += 1
                elif self.y_segments[i] - self.y_segments [i - 1] > 1:
                    self.y_segments[i] -= 1
                elif self.y_segments[i] - self.y_segments [i - 1] < -1:
                    self.y_segments[i] += 1
            elif (abs(self.x_segments[i] - self.x_segments[i - 1]) > 1 or
                  abs(self.y_segments[i] - self.y_segments[i - 1]) > 1):
                possible = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
                for p in possible:
                    if (abs(self.x_segments[i] + p[0] - self.x_segments[i - 1]) <= 1 and
                            abs(self.y_segments[i] + p[1] - self.y_segments[i - 1]) <= 1):
                        self.x_segments[i] += p[0]
                        self.y_segments[i] += p[1]
                        break

    def move_single(self, direction):
        if direction == 'U':
            self.y_segments[0] -= 1
        elif direction == 'D':
            self.y_segments[0] += 1
        elif direction == 'L':
            self.x_segments[0] -= 1
        elif direction == 'R':
            self.x_segments[0] += 1
        self.propagate()
        self.tail_visited.add((self.x_segments[-1], self.y_segments[-1]))
        self.head_visited.add((self.x_segments[0], self.y_segments[0]))

    def move_steps(self, direction, steps):
        for _ in range(steps):
            self.move_single(direction)
    
    def get_number_tail_visited(self):
        return len(self.tail_visited)

    def __str__(self):
        output = ""
        substitutions = dict()
        for i in range(self.length):
            if i == 0:
                substitutions[(self.x_segments[i], self.y_segments[i])] = 'H'
            else:
                substitutions[(self.x_segments[i], self.y_segments[i])] = str(i)
        for y in range(min(self.y_segments), max(self.y_segments) + 1):
            for x in range(min(self.x_segments), max(self.x_segments) + 1):
                if (x, y) in substitutions:
                    output += substitutions[(x, y)]
                else:
                    output += '.'
            output += '\n'
        return output
    
    def __repr__(self):
        return str(list(zip(self.x_segments, self.y_segments)))

def solve(array):
    snake1 = Snake(0, 0, 2)
    snake2 = Snake(0, 0, 10)
    for line in array:
        direction, n = line.split()
        n = int(n)
        snake1.move_steps(direction, n)
        snake2.move_steps(direction, n)

    print("Part 1:", snake1.get_number_tail_visited())
    print("Part 2:", snake2.get_number_tail_visited())
    
def visualise(array):
    os.system("")
    snake3 = Snake(0, 0, 10)
    for line in array:
        direction, n = line.split()
        n = int(n)
        for _ in range(n):
            os.system('cls')
            snake3.move_single(direction)
            output = ""
            substitutions = dict()
            for i in range(snake3.length):
                if i == 0:
                    substitutions[(snake3.x_segments[i], snake3.y_segments[i])] = 'H'
                else:
                    substitutions[(snake3.x_segments[i], snake3.y_segments[i])] = str(i)
            boxy_size = 40
            boxx_size = 100
            ymin = min(snake3.y_segments)
            ymax = max(snake3.y_segments)
            box_ymin = ymin - math.floor((boxy_size - ymax + ymin) / 2)
            box_ymax = ymax + math.ceil((boxy_size - ymax + ymin) / 2)
            xmin = min(snake3.x_segments)
            xmax = max(snake3.x_segments)
            box_xmin = xmin - math.floor((boxx_size - xmax + xmin) / 2)
            box_xmax = xmax + math.ceil((boxx_size - xmax + xmin) / 2)
            for y in range(box_ymin, box_ymax):
                for x in range(box_xmin, box_xmax):
                    if (x, y) in substitutions:
                        output += substitutions[(x, y)]
                    elif (x,y) in snake3.tail_visited:
                        output += '\033[33m█\033[0m'
                    else:
                        output += ' '
                    
                output += '\n'
            print(output, end='\r')

if __name__ == '__main__':
    filename = "test.txt"
    arr = arrayise(filename)
    solve(arr)
    user = input("Visualise? [y/n]")
    if user.lower() == 'y':
        visualise(arr)
