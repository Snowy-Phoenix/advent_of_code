import re

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day8(array):
    operations = []
    for line in array:
        operation, value = line.split(" ")
        value = int(value)
        operations.append((operation, value))
    
    instruction_ptr = 0
    accumulator = 0
    executed_instructions = set()
    while True:
        if instruction_ptr in executed_instructions:
            break
        else:
            executed_instructions.add(instruction_ptr)
        operation, value = operations[instruction_ptr]
        if operation == "acc":
            accumulator += value
        elif operation == "jmp":
            instruction_ptr += value - 1
        instruction_ptr += 1
    print("Part 1:", accumulator)

    
    for op_line in range(len(operations)):

        unmodified_operation = operations[op_line]
        if (unmodified_operation[0] == "nop"):
            operations[op_line] = ("jmp", unmodified_operation[1])
        elif (unmodified_operation[0] == "jmp"):
            operations[op_line] = ("nop", unmodified_operation[1])
        else:
            continue

        instruction_ptr = 0
        accumulator = 0
        executed_instructions = set()
        halted = False
        while True:
            if instruction_ptr in executed_instructions:
                break
            else:
                executed_instructions.add(instruction_ptr)
            operation, value = operations[instruction_ptr]
            if operation == "acc":
                accumulator += value
            elif operation == "jmp":
                instruction_ptr += value - 1
            instruction_ptr += 1
            if (instruction_ptr >= len(operations)):
                halted = True
                break
        if halted:
            print("Part 2:", accumulator)
            break
        operations[op_line] = unmodified_operation

if __name__ == "__main__":
    filename = "input8.txt"
    arr = arrayise(filename)
    day8(arr)