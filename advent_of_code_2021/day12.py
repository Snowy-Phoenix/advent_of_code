import math
import re
import numpy as np
import copy

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day12(array):
    edges = dict()
    for line in array:
        a, b = line.split("-")

        if a not in edges:
            edges[a] = [b]
        else:
            edges[a].append(b)

        if b not in edges:
            edges[b] = [a]
        else:
            edges[b].append(a)
    print("Part 1:", count_paths("start", edges, set()))
    print("Part 2:", count_paths("start", edges, set(), part2=True))

def count_paths(node, edges, visited, part2=False, visited_twice=""):
    paths = 0
    if node.islower():
        visited.add(node)
    node_edges = edges[node]
    for n in node_edges:
        if n == "start":
            continue
        if n == "end":
            paths += 1
            continue
        elif n in visited:
            if part2:
                paths += count_paths(n, edges, visited, part2=False, visited_twice=n)
            continue
        else:
            paths += count_paths(n, edges, visited, part2, visited_twice)
    if node.islower() and node != visited_twice:
        visited.remove(node)
    return paths

if __name__ == "__main__":
    filename = "input12.txt"
    arr = arrayise(filename)
    day12(arr)
    

