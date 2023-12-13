import copy
import re

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def evaluate_basic_expression(left, operation, right):
    if operation == "*":
        result = left * right
    else:
        result = left + right
    return result

def get_bracketed_expression(expression):
    bracketed_expression = []
    brackets = 0
    for i in range(len(expression)):
        nested_token = expression[i]
        for c in nested_token:
            if (c == '('):
                brackets += 1
            elif (c == ')'):
                brackets -= 1
        bracketed_expression.append(nested_token)
        if brackets == 0:
            break
    bracketed_expression[0] = bracketed_expression[0][1:]
    bracketed_expression[-1] = bracketed_expression[-1][:len(bracketed_expression[-1]) - 1]
    return bracketed_expression

def evaluate_expression(full_expression):
    expression = copy.copy(full_expression)

    if len(expression) == 1:
        return int(expression[0])

    l_token = None
    operation = None
    i = 0
    while i < len(expression):
        token = expression[i]
        if l_token == None:
            if token.isdigit():
                l_token = int(token)
            else:
                l_token = 0
                operation = "+"
                continue
        elif operation == None:
            operation = token
        else:
            if token.isdecimal():
                l_token = evaluate_basic_expression(l_token, operation, int(token))
                operation = None
            else:
                bracketed_expression = get_bracketed_expression(expression[i:])
                result = evaluate_expression(bracketed_expression)
                l_token = evaluate_basic_expression(l_token, operation, result)
                operation = None
                i += len(bracketed_expression) - 1
        i += 1
    return l_token

def evaluate_addition_first(full_expression):
    expression = copy.copy(full_expression)
    if (len(expression) == 1):
        return int(expression[0])

    left_expression = []
    right_expression = []

    i = 0
    while i < len(expression):
        token = expression[i]
        if token[0] == '(':
            bracketed_expression = get_bracketed_expression(expression[i:])
            value = evaluate_addition_first(bracketed_expression)
            for j in range(len(bracketed_expression) - 1):
                expression.pop(i)
                expression[i] = str(value)
        elif token == '+':
            if expression[i-1].isdigit():
                left_expression.append(expression[i-1])
            else:
                brackets = 0
                for j in range(i-1, -1, -1):
                    l_token = expression[j]
                    for c in l_token:
                        if c == ")":
                            brackets += 1
                        elif c == "(":
                            brackets -= 1
                    left_expression.insert(0, l_token)
                    if brackets <= 0:
                        break

            if expression[i+1].isdigit():
                right_expression.append(expression[i+1])
            else:
                brackets = 0
                for j in range(i+1, len(expression)):
                    r_token = expression[j]
                    for c in r_token:
                        if c == "(":
                            brackets += 1
                        elif c == ")":
                            brackets -= 1
                    right_expression.append(r_token)
                    if brackets <= 0:
                        break

            value = evaluate_addition_first(left_expression) + evaluate_addition_first(right_expression)
            i = i - len(left_expression)
            for k in range(len(right_expression) + len(left_expression)):
                expression.pop(i)
            expression[i] = str(value)
            left_expression.clear()
            right_expression.clear()
        i += 1

    return evaluate_expression(expression)

def day18(array):
    total = 0
    for line in array:
        total += evaluate_expression(line.split(' '))
    print("Part 1:", total)

    total = 0
    for line in array:
        total += evaluate_addition_first(line.split(' '))
    print("Part 2:", total)


if __name__ == "__main__":
    filename = "input18.txt"
    arr = arrayise(filename)
    day18(arr)