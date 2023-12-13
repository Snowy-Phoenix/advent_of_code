import math
import re
import numpy as np
import copy
import random

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

class Alu:
    def __init__(self, instructions):
        self.instructions = instructions
        self.variables = [0,0,0,0]
        self.var_map = {'x':0, 'y':1, 'z':2, 'w':3}

    def reset(self):
        self.variables = [0,0,0,0]

    def run(self, input_stream=None):
        input_curser = 0
        for instruction in self.instructions:
            operation = instruction[0]
            if operation == 'inp':
                read_int = None
                if input_stream == None:
                    read_int = int(input())
                elif input_curser >= len(input_stream):
                    read_int = int(input())
                else:
                    read_int = int(input_stream[input_curser])
                    input_curser += 1
                variable_i = self.var_map[instruction[1]]
                self.variables[variable_i] = read_int
            else:
                var_a = instruction[1]
                var_b = instruction[2]
                try:
                    var_b = int(var_b)
                except ValueError:
                    var_b = self.variables[self.var_map[var_b]]
                if operation == 'add':
                    self.variables[self.var_map[var_a]] += var_b
                elif operation == 'mul':
                    self.variables[self.var_map[var_a]] *= var_b
                elif operation == 'div':
                    self.variables[self.var_map[var_a]] //= var_b
                elif operation == 'mod':
                    self.variables[self.var_map[var_a]] %= var_b
                elif operation == 'eql':
                    result = int(self.variables[self.var_map[var_a]] == var_b)
                    self.variables[self.var_map[var_a]] = result
        return self.variables

    def __str__(self):
        return str(self.variables)

def generate_inputs(num_inputs, prev_best, optimise_highest):
    generated = []
    if prev_best == None:
        for _ in range(num_inputs):
            node = []
            for _ in range(14):
                node.append(random.randint(1, 9))
            generated.append(tuple(node))
    else:
        number = 0
        for n in prev_best.inp:
            number *= 10
            number += n
        number_str = str(number)
        for _ in range(num_inputs):
            random_input = []
            is_unequal = False
            if optimise_highest:
                for i, c in enumerate(number_str):
                    if is_unequal:
                        random_input.append(random.randint(1, 9))
                    else:
                        random_input.append(random.randint(int(c), 9))
                        if random_input[i] != number_str[i]:
                            is_unequal = True
            else:
                for i, c in enumerate(number_str):
                    if is_unequal:
                        random_input.append(random.randint(1, 9))
                    else:
                        random_input.append(random.randint(1, int(c)))
                        if random_input[i] != number_str[i]:
                            is_unequal = True

            generated.append(random_input)
    return generated

class Node:
    def __init__(self, inp, error, optimise_greatest):
        self.inp = inp
        self.error = error
        self.optimise_greatest = optimise_greatest
    
    def __lt__(self, other):
        if self.error < other.error:
            return True
        elif self.error == other.error:
            for i in range(14):
                if self.inp[i] > other.inp[i]:
                    return self.optimise_greatest
                elif self.inp[i] < other.inp[i]:
                    return not self.optimise_greatest
        return False

    def __str__(self):
        return str(self.inp)

def generate_offspring(inp, optimise_greatest, prev_best):
    new_input = []
    for n in inp:
        roll = random.randint(1, 5)
        if roll == 1:
            new_input.append(random.randint(1, 9))
        else:
            new_input.append(n)

    if prev_best != None:
        prev_best_inp = prev_best.inp
        for i, n in enumerate(new_input):
            if optimise_greatest:
                if prev_best_inp[i] > new_input[i]:
                    new_input[i] = random.randint(prev_best_inp[i], 9)
                elif prev_best_inp[i] < new_input[i]:
                    break
            else:
                if prev_best_inp[i] < new_input[i]:
                    new_input[i] = random.randint(1, prev_best_inp[i])
                elif prev_best_inp[i] > new_input[i]:
                    break
    return tuple(new_input)

def simulate(alu, optimise_greatest=True, max_inputs=500, max_no_improvement=50, prev_best=None):
    if prev_best != None:
        if prev_best.error != 0:
            prev_best = None
    curr_inputs = generate_inputs(max_inputs, prev_best, optimise_greatest)
    steps_no_improvement = 0
    best_node = Node(None, None, False)
    if prev_best:
        curr_inputs.append(prev_best.inp)
    while True:
        results = []
        for inp in curr_inputs:
            results.append(Node(inp, alu.run(input_stream=inp)[2], optimise_greatest))
            alu.reset()
        results = sorted(results)
        
        if results[0].inp == best_node.inp:
            steps_no_improvement += 1
        else:
            best_node = results[0]
            # print("New best:", best_node.inp, best_node.error)
            steps_no_improvement = 0

        if steps_no_improvement > max_no_improvement:
            return results[0]
        
        next_generation = []
        for i in range(max_inputs // 2):
            next_generation.append(results[i].inp)
            next_generation.append(generate_offspring(results[i].inp, optimise_greatest, prev_best))
        curr_inputs = next_generation

def day24(array):
    instructions = []
    for instruction in array:
        instructions.append(instruction.split(' '))
    
    alu = Alu(instructions)
    best_node1 = simulate(alu)
    max_no_improvements = 5
    no_improvement_streak = 0
    while True:
        curr_node = simulate(alu, prev_best=best_node1)
        if curr_node.error != 0:
            # Theoretically an infinite loop if the random generator is terrible.
            no_improvement_streak += 1
            continue
        elif best_node1.inp == curr_node.inp:
            no_improvement_streak += 1
        else:
            best_node1 = curr_node
            no_improvement_streak = 0
        if no_improvement_streak >= max_no_improvements:
            string = ""
            for c in best_node1.inp:
                string += str(c)
            print("Part 1:", string)
            break

    alu = Alu(instructions)
    best_node1 = simulate(alu, optimise_greatest=False)
    max_no_improvements = 5
    no_improvement_streak = 0
    while True:
        curr_node = simulate(alu, optimise_greatest=False, prev_best=best_node1)
        if curr_node.error != 0:
            # Theoretically an infinite loop if the random generator is terrible.
            no_improvement_streak += 1
            continue
        elif best_node1.inp == curr_node.inp:
            no_improvement_streak += 1
        else:
            best_node1 = curr_node
            no_improvement_streak = 0
        if no_improvement_streak >= max_no_improvements:
            string = ""
            for c in best_node1.inp:
                string += str(c)
            print("Part 2:", string)
            break


if __name__ == "__main__":
    filename = "input24.txt"
    arr = arrayise(filename)
    day24(arr)
