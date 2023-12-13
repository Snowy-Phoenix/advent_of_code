import math
import re
import numpy as np
from intcode import IntcodeInterpreter

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def count_orbits(root, edges, counts):
    if root not in edges:
        counts[root] = 0
        return 0
    root_edges = edges[root]
    count = 0
    for node in root_edges:
        count += 1
        count += count_orbits(node, edges, counts)
    counts[root] = count
    return count

def get_shortest_path(from_node, to_node, parents):
    visited_nodes = dict() # Node, count
    current_node = from_node
    distance = 0
    while True:
        visited_nodes[current_node] = distance
        if current_node in parents:
            current_node = parents[current_node]
            distance += 1
        else:
            break
    distance = 0
    current_node = to_node
    while True:
        if current_node in visited_nodes:
            return distance + visited_nodes[current_node]
        distance += 1
        current_node = parents[current_node]

def day6(array):
    edges = dict() # left, orbits
    parents = dict()
    for line in array:
        left, right = line.split(")")
        if left in edges:
            edges[left].append(right)
        else:
            edges[left] = [right]
        parents[right] = left

    root_node = "COM"
    counts = dict()
    count_orbits(root_node, edges, counts)
    print("Part 1:", sum(counts.values()))

    print(get_shortest_path(parents["YOU"], parents["SAN"], parents))



if __name__ == "__main__":
    filename = "input6.txt"
    arr = arrayise(filename)
    day6(arr)
    

