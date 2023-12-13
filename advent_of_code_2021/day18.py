import math
import re
import numpy as np
import copy
import itertools
import heapq

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def char_array_to_string(char_array):
    new_expression = ""
    for c in char_array:
        new_expression += c
    return new_expression

def get_left(expression, i):
    while i >= 0:
        c = expression[i]
        if c.isdigit():
            while expression[i-1].isdigit():
                i -= 1
            return i
        i -= 1
    return None

def get_right(expression, i):
    while i < len(expression):
        c = expression[i]
        if c.isdigit():
            return i
        i += 1
    return None

def add_n_to_expression(expression, index, number):
    new_number = 0
    
    insertions = 0
    while expression[index].isdigit():
        new_number *= 10
        new_number += int(expression.pop(index))
        insertions -= 1
    new_number += number
    str_number = str(new_number)
    for i in range(len(str_number) - 1, -1, -1):
        expression.insert(index, str_number[i])
        insertions += 1
    return insertions

def get_nested_numbers(nested_expression):
    first_n = 0
    i = 1
    while nested_expression[i] != ',':
        first_n *= 10
        first_n += int(nested_expression[i])
        i += 1
    i += 1
    second_n = 0
    while nested_expression[i] != ']':
        second_n *= 10
        second_n += int(nested_expression[i])
        i += 1
    return (first_n, second_n)

def explode(raw_expression):
    expression = [char for char in raw_expression]
    nesting = 0
    nested_expression = []
    nested_exppression_starti = -1
    nested_exppression_endi = -1
    found_nested = False
    for i in range(len(expression)):
        c = expression[i]
        if c == '[':
            nesting += 1
            if nesting >= 5:
                nested_expression.append(c)
                found_nested = True
                nested_exppression_starti = i
        elif c == ']':
            nesting -= 1
            if found_nested:
                nested_expression.append(c)
                if nesting <= 4:
                    nested_exppression_endi = i + 1
                    break
        else:
            if found_nested:
                nested_expression.append(c)

    if found_nested:
        left_nested_number, right_nested_number = get_nested_numbers(nested_expression)
        left_i = get_left(expression, nested_exppression_starti)
        right_i = get_right(expression, nested_exppression_endi)
        pops = nested_exppression_endi - nested_exppression_starti - 1
        if left_i == None:
            add_n_to_expression(expression, right_i, right_nested_number)
            for i in range(pops):
                expression.pop(nested_exppression_starti)
            expression[nested_exppression_starti] = '0'
        elif right_i == None:
            offset = add_n_to_expression(expression, left_i, left_nested_number)
            for i in range(pops):
                expression.pop(nested_exppression_starti + offset)
            expression[nested_exppression_starti + offset] = '0'
        else:
            add_n_to_expression(expression, right_i, right_nested_number)
            offset = add_n_to_expression(expression, left_i, left_nested_number)
            for i in range(pops):
                expression.pop(nested_exppression_starti + offset)
            expression[nested_exppression_starti + offset] = '0'
        return (True, char_array_to_string(expression))
    else:
        return (False, raw_expression)

def split(raw_expression):
    expression = [char for char in raw_expression]
    start_digit_i = -1
    end_digit_i = -1
    found_digit = False
    for i in range(1, len(expression)):
        if expression[i].isdigit() and expression[i - 1].isdigit():
            found_digit = True
            start_digit_i = i - 1
            end_digit_i = i
            break
    if found_digit:
        while expression[end_digit_i + 1].isdigit():
            end_digit_i += 1
        number_to_split = int(raw_expression[start_digit_i:end_digit_i + 1])
        left_n = number_to_split // 2
        right_n = number_to_split // 2
        if number_to_split % 2 == 1:
            right_n += 1
        for _ in range(end_digit_i - start_digit_i + 1):
            expression.pop(start_digit_i)
        expression.insert(start_digit_i, ']')
        for c in reversed(str(right_n)):
            expression.insert(start_digit_i, c)
        expression.insert(start_digit_i, ',')
        for c in reversed(str(left_n)):
            expression.insert(start_digit_i, c)
        expression.insert(start_digit_i, '[')

        return (True, char_array_to_string(expression))

    else:
        return (False, raw_expression)
        
def add_expressions(e1, e2):
    return '[' + e1 + ',' + e2 + ']'

def calculate_magnitude(expression):
    if expression.isdigit():
        return int(expression)
    nesting = 0
    removed_outer_brackets = expression[1:-1]
    for i in range(len(removed_outer_brackets)):
        c = removed_outer_brackets[i]
        if c == '[':
            nesting += 1
        elif c == ']':
            nesting -= 1
        elif c == ',' and nesting == 0:
            return 3 * calculate_magnitude(removed_outer_brackets[:i]) + \
                   2 * calculate_magnitude(removed_outer_brackets[i + 1:])

def reduce_expression(expression):
    while True:
        explode_result = explode(expression)
        if explode_result[0] == True:
            expression = explode_result[1]
            continue
        split_result = split(expression)
        if split_result[0] == True:
            expression = split_result[1]
            continue
        break
    return expression

def day18a(array):
    expressions = []
    for line in array:
        expressions.append(line)
    
    current_expression = ""
    for expression in expressions:
        if current_expression == "":
            current_expression += expression
        else:
            current_expression = add_expressions(current_expression, expression)
        current_expression = reduce_expression(current_expression)
        
    print("Part 1:", calculate_magnitude(current_expression))

def day18b(array):
    expressions = []
    for line in array:
        expressions.append(line)
    
    maximum_magnitude = 0
    for i in range(len(expressions)):
        for j in range(len(expressions)):
            if i == j:
                continue
            evaluated_expression = add_expressions(expressions[i], expressions[j])
            evaluated_expression = reduce_expression(evaluated_expression)
            maximum_magnitude = max(maximum_magnitude, calculate_magnitude(evaluated_expression))
    print("Part 2:", maximum_magnitude)
            

if __name__ == "__main__":
    filename = "input18.txt"
    arr = arrayise(filename)
    day18a(arr)
    day18b(arr)
