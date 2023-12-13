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

def evaluate(operations, literals):
    unsolved_operations = operations.copy()
    current_literals = literals.copy()
    left_root = 0
    right_root = 0
    while 'root' not in current_literals:
        changed = False
        keys = list(unsolved_operations.keys())
        for monkey in keys:
            operand1, operator, operand2 = operations[monkey].split()
            if operand1 in current_literals and operand2 in current_literals:
                if (monkey) == 'root':
                    left_root = current_literals[operand1]
                    right_root = current_literals[operand2]
                changed = True
                if operator == '+':
                    current_literals[monkey] = current_literals[operand1] + current_literals[operand2]
                elif operator == '-':
                    current_literals[monkey] = current_literals[operand1] - current_literals[operand2]
                elif operator == '*':
                    current_literals[monkey] = current_literals[operand1] * current_literals[operand2]
                elif operator == '/':
                    current_literals[monkey] = current_literals[operand1] // current_literals[operand2]
                unsolved_operations.pop(monkey)
    if not changed:
        print("Cannot derive root.")
        return -1
    return current_literals['root'], left_root, right_root

def solve(arr):
    operations = dict() # Monkey, str operation.
    literals = dict() # Monkey, number
    for line in arr:
        monkey, operation = line.split(": ")
        if (operation.isnumeric()):
            literals[monkey] = int(operation)
        else:
            operations[monkey] = operation
    answers = evaluate(operations, literals)
    print("Part 1:", answers[0])
    lower_bound = 0
    upper_bound = 1
    human_i = 1
    cmp_i = 2
    literals['humn'] = 1
    answer1 = evaluate(operations, literals)
    literals['humn'] = 2
    answer2 = evaluate(operations, literals)
    if answer1[1] != answer2[1] and answer1[2] == answer2[2]:
        human_i = 1
        cmp_i = 2
    elif answer1[1] == answer2[1] and answer1[2] != answer2[2]:
        human_i = 2
        cmp_i = 1
    
    literals['humn'] = lower_bound
    answer_lower = evaluate(operations, literals)
    sign_lower = answer_lower[human_i] - answer_lower[cmp_i] == abs(answer_lower[human_i] - answer_lower[cmp_i])

    while True:
        literals['humn'] = upper_bound
        answer_higher = evaluate(operations, literals)
        sign_higher = answer_higher[human_i] - answer_higher[cmp_i] == abs(answer_higher[human_i] - answer_higher[cmp_i])
        if (sign_lower != sign_higher):
            break
        upper_bound *= 2
    lowest_answer = upper_bound
    found = False
    while lower_bound <= upper_bound:
        midpoint = ((lower_bound + upper_bound) // 2)
        literals['humn'] = midpoint
        answer = evaluate(operations, literals)
        if (answer[1] == answer[2]):
            lowest_answer = min(lowest_answer, midpoint)
            found = True
        sign_middle = answer[human_i] - answer[cmp_i] == abs(answer[human_i] - answer[cmp_i])
        if (sign_middle == sign_lower):
            lower_bound = midpoint + 1
        else:
            upper_bound = midpoint - 1
    if (found):
        print("Part 2:", lowest_answer)
    else:
        print("Unable to find an answer")

if __name__ == '__main__':
    filename = "input21.txt"
    arr = arrayise(filename)
    solve(arr)
    