from collections import deque
from collections import defaultdict
import math
import os

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def solve_rushed(array):
    t_arr = [1,6,7,7,0,4,3,4]
    f_arr = [6,3,5,2,1,0,2,5]
    m0 = deque([83, 62, 93])
    op0 = lambda x: x * 17
    test0 = lambda x: x % 2 == 0

    m1 = deque([90, 55])
    op1 = lambda x: x + 1
    test1 = lambda x: x % 17 == 0

    m2 = deque([91, 78, 80, 97, 79, 88])
    op2 = lambda x: x + 3
    test2 = lambda x: x % 19 == 0

    m3 = deque([64, 80, 83, 89, 59])
    op3 = lambda x: x + 5
    test3 = lambda x: x % 3 == 0

    m4 = deque([98, 92, 99, 51])
    op4 = lambda x: x * x
    test4 = lambda x: x % 5 == 0

    m5 = deque([68, 57, 95, 85, 98, 75, 98, 75])
    op5 = lambda x: x + 2
    test5 = lambda x: x % 13 == 0

    m6 = deque([74])
    op6 = lambda x: x + 4
    test6 = lambda x: x % 7 == 0

    m7 = deque([68, 64, 60, 68, 87, 80, 82])
    op7 = lambda x: x * 19
    test7 = lambda x: x % 11 == 0

    m = [m0,m1,m2,m3,m4,m5,m6,m7]
    op = [op0,op1,op2,op3,op4,op5,op6,op7]
    test = [test0,test1,test2,test3,test4,test5,test6,test7]
    inspections = [0,0,0,0,0,0,0,0]
    for _ in range(10000):
        for i in range(8):
            while len(m[i]) > 0:
                item = m[i].popleft()
                item = op[i](item)
                item = item % 9699690
                if test[i](item):
                    m[t_arr[i]].append(item)
                else:
                    m[f_arr[i]].append(item)
                inspections[i] += 1
    print(inspections)

class Monkey:
    def __init__(self, items, operation, test, if_true, if_false):
        self.items = items
        self.operation = operation
        self.div_test = test
        self.if_true = if_true
        self.if_false = if_false
        self.inspections = 0

    def inspect(self, item_modifier=lambda x: x):
        items_thrown = []
        thrown_to = []

        while len(self.items) > 0:
            item = self.items.popleft()
            item = self.operation(item)
            item = item_modifier(item)
            items_thrown.append(item)
            if (item % self.div_test == 0):
                thrown_to.append(self.if_true)
            else:
                thrown_to.append(self.if_false)
            self.inspections += 1
        return items_thrown, thrown_to
    
    def catch(self, item):
        self.items.append(item)
    def get_inspections(self):
        return self.inspections

def parse_starting_items(line):
    items = deque()
    starting_items = line.strip().split()[2:]
    for item in starting_items:
        items.append(int(item.strip(',')))
    return items

def parse_operation(line):
    tokens = line.strip().split()[4:]
    if tokens[1] == 'old':
        return lambda x: x * x
    elif tokens[0] == '+':
        return lambda x: x + int(tokens[1])
    elif tokens[0] == '*':
        return lambda x: x * int(tokens[1])
    return None
    
def parse_test(line):
    try:
        return int(line.strip().split()[3])
    except ValueError:
        return None

def parse_throw(line):
    try:
        return int(line.strip().split()[5])
    except ValueError:
        return None

def parse_monkey(lines, i):
    items = parse_starting_items(lines[i + 1])
    operation = parse_operation(lines[i + 2])
    if operation == None:
        print("Invalid operation: {} at line {}".format(lines[i + 2], i + 2 + 1))
        return None
    test = parse_test(lines[i + 3])
    if test == None:
        print("Invalid operation: {} at line {}".format(lines[i + 3], i + 3 + 1))
        return None
    true_to = parse_throw(lines[i + 4])
    if true_to == None:
        print("Invalid operation: {} at line {}".format(lines[i + 4], i + 4 + 1))
        return None
    false_to = parse_throw(lines[i + 5])
    if false_to == None:
        print("Invalid operation: {} at line {}".format(lines[i + 5], i + 5 + 1))
        return None
    return Monkey(items, operation, test, true_to, false_to)
    
def parse_monkeys(array):
    monkeys = []
    line_i = 0
    while line_i < len(array):
        line = array[line_i].split()
        if line[0].lower() == 'monkey':
            monkey = parse_monkey(array, line_i)
            if monkey != None:
                monkeys.append(monkey)
            line_i += 7
        else:
            line_i += 1
    return monkeys

def simulate_rounds(monkeys, rounds, modifier=lambda x: x):
    for _ in range(rounds):
        for monkey in monkeys:
            items, to = monkey.inspect(modifier)
            for i, item in enumerate(items):
                monkeys[to[i]].catch(item)

def part1(array):
    monkeys = parse_monkeys(array)
    simulate_rounds(monkeys, 20, modifier=lambda x: x // 3)
    inspections = []
    for monkey in monkeys:
        inspections.append(monkey.get_inspections())
    inspections.sort(reverse=True)
    print("Part 1:", inspections[0] * inspections[1])

def part2(array):
    monkeys = parse_monkeys(array)
    modulo = 1
    for monkey in monkeys:
        modulo *= monkey.div_test
    simulate_rounds(monkeys, 10000, modifier=lambda x: x % modulo)
    inspections = []
    for monkey in monkeys:
        inspections.append(monkey.get_inspections())
    inspections.sort(reverse=True)
    print("Part 2:", inspections[0] * inspections[1])

def solve(array):
    part1(array)
    part2(array)

if __name__ == '__main__':
    filename = "input11.txt"
    # print(166945 * 154173)
    arr = arrayise(filename)
    # solve_rushed(arr)
    solve(arr)
