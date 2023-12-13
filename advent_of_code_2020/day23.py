import re
import numpy as np
import copy

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

class CircularDoubleLinkedList:
    
    def __init__(self):
        self.root = None
        self.size = 0

    def append(self, value):
        node = Node(value)
        if self.root == None:
            self.root = node
            node.prev = node
            node.next = node
        else:
            last_node = self.root.prev
            self.root.prev = node
            last_node.next = node

            node.prev = last_node
            node.next = self.root
        self.size += 1

    def remove(self, node):

        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
        self.size -= 1
    
    def insert(self, node, inserting_node):
        next_node = node.next

        node.next = inserting_node
        next_node.prev = inserting_node

        inserting_node.next = next_node
        inserting_node.prev = node
        self.size += 1

    def compile_dictionary(self):
        dictionary = dict()
        curr_node = self.root
        for i in range(self.size):
            dictionary[curr_node.value] = curr_node
            curr_node = curr_node.next
        return dictionary

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.CircularDoubleLinkedListIterator(self)

    class CircularDoubleLinkedListIterator:
        def __init__(self, linked_list):
            self.__list = linked_list
            self.__curr_node = linked_list.root
            self.__index = 0

        def __next__(self):
            if self.__index >= len(self.__list):
                raise StopIteration
            value = self.__curr_node.value
            self.__curr_node = self.__curr_node.next
            self.__index += 1
            return value
            
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

    def __repr__(self):
        return str(self.value)

def get_next_numbers(circular_array, index, numbers_to_select):
    selected_numbers = []
    for i in range(numbers_to_select):
        selected_numbers.append(circular_array[(index + i) % len(circular_array)])
    return selected_numbers

def get_destination(current_number, max_number, selected_numbers):
    destination_number = current_number - 1
    while True:
        if destination_number == current_number:
            raise ValueError("Unable to obtain a destination number.")

        if destination_number == 0:
            destination_number = max_number
        
        if destination_number in selected_numbers:
            destination_number -= 1
        else:
            return destination_number
        
def swap_numbers(circular_array, index, numbers, destination):
    curr_index_offset = len(numbers)
    c_array_len = len(circular_array)
    while True:
        if curr_index_offset > len(circular_array):
            # We have traversed the whole circular array.
            raise ValueError("Destination number not found")
        swapped_number = circular_array[(index + curr_index_offset) % c_array_len]
        circular_array[(index + curr_index_offset - len(numbers)) % c_array_len] = swapped_number
        if swapped_number == destination:
            break
        curr_index_offset += 1
    for i in range(len(numbers)):
        circular_array[(index + curr_index_offset - len(numbers) + i + 1) % c_array_len] = numbers[i]

def solve_part1(circular_array):
    c_array_len = len(circular_array)
    string = ""
    i = 0
    while i < len(circular_array):
        if circular_array[i] == 1:
            break
        i += 1
    i += 1
    n = circular_array[i % c_array_len]
    while n != 1:
        string += str(n)
        i += 1
        n = circular_array[i % c_array_len]
    return string

def solve_part2(circular_array):
    for i in range(len(circular_array)):
        n = circular_array[i]
        if n == 1:
            return circular_array[(i + 1) % len(circular_array)] * circular_array[(i + 2) % len(circular_array)]

def day23a(array, moves=100, numbers_selected=3, print_array=False):

    circular_array = copy.copy(array)
    max_number = max(circular_array)
    if len(circular_array) <= numbers_selected + 1:
        raise ValueError("Numbers selected exceeds number of elements in array.")

    c_array_len = len(circular_array)
    if print_array:
        print(circular_array)
    for index in range(moves):
        current_number = circular_array[index % c_array_len]
        next_numbers = get_next_numbers(circular_array, index + 1, numbers_selected)
        destination_number = get_destination(current_number, max_number, next_numbers)
        swap_numbers(circular_array, index + 1, next_numbers, destination_number)
        if print_array:
            print(circular_array)

    
    print("Part 1:", solve_part1(circular_array))
    
def day23b(array,  moves=100, numbers_selected=3, max_number=20):

    circular_list = CircularDoubleLinkedList()
    for i in range(1, max_number + 1):
        current_number = i
        if i <= len(array):
            current_number = array[i - 1]
        circular_list.append(current_number)

    numbers = circular_list.compile_dictionary()
    current_node = circular_list.root
    for i in range(moves):
        selected_numbers = []
        selected_nodes = []
        for j in range(numbers_selected):
            selected_numbers.append(current_node.next.value)
            selected_nodes.append(current_node.next)
            circular_list.remove(current_node.next)
        destination = get_destination(current_node.value, max_number, selected_numbers)
        destination_node = numbers[destination]
        for j in range(numbers_selected):
            if j == 0:
                circular_list.insert(destination_node, selected_nodes[j])
            else:
                circular_list.insert(selected_nodes[j-1], selected_nodes[j])
        current_node = current_node.next
    
    node1 = numbers[1]
    print("Part 2:", node1.next.value * node1.next.next.value)
    
        


if __name__ == "__main__":
    filename = "input23.txt"
    arr = arrayise(filename)
    day23a([int(x) for x in arr[0]], moves=100)
    day23b([int(x) for x in arr[0]], moves=10000000, max_number=1000000)
