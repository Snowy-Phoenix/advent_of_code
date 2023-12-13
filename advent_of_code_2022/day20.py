from collections import deque
from collections import defaultdict
import heapq
import copy
import math

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

class LinkedListNode:
    def __init__(self, n):
        self.n = n
        self.prev = None
        self.next = None

def get_coordinates(arr, cycles, decryption_key):
    number_i = dict() # i, linked list.
    n_node = dict() # n, node
    numbers = []
    for i, line in enumerate(arr):
        node = LinkedListNode(int(line) * decryption_key)
        n_node[int(line) * decryption_key] = node
        numbers.append(node)
        number_i[i] = node
        if (i != 0):
            node.prev = numbers[-2]
            numbers[-2].next = node
    numbers[0].prev = numbers[-1]
    numbers[-1].next = numbers[0]
    for _ in range(cycles):
        for i in range(len(number_i)):
            curr_node = number_i[i]
            n = curr_node.n
            next_node = curr_node.prev
            curr_node.prev.next = curr_node.next
            curr_node.next.prev = curr_node.prev
            for _ in range(abs(n % (len(number_i) - 1))):
                next_node = next_node.next
            curr_node.prev = next_node
            curr_node.next = next_node.next
            next_node.next.prev = curr_node
            next_node.next = curr_node
    curr_node = n_node[0]
    summation = 0
    for i in range(3001):
        if i % 1000 == 0:
            summation += curr_node.n
        curr_node = curr_node.next
    return summation

def solve(arr):
    print("Part 1:", get_coordinates(arr, 1, 1))
    print("Part 2:", get_coordinates(arr, 10, 811589153))


if __name__ == '__main__':
    filename = "input20.txt"
    arr = arrayise(filename)
    solve(arr)
    