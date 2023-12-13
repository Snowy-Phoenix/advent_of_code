import re

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day15_unoptimised(array, turns=2020):
    for i in range(len(array) - 1, turns - 1):
        number = array[i]
        found = False
        for j in range(i - 1, -1, -1):
            if array[j] == number:
                array.append(i - j)
                found = True
                break
        if not found:
            array.append(0)
    print("{}th number is: {}".format(turns, array[-1]))

def day15(array, turns=2020):
    number_position = dict() # Number, turn_said
    for i in range(len(array) - 1):
        number_position[array[i]] = i + 1
    current_number = array[-1]
    for t in range(len(array), turns):
        if (current_number not in number_position):
            number_position[current_number] = t
            current_number = 0
        else:
            new_number = t - number_position[current_number]
            number_position[current_number] = t
            current_number = new_number
    print("{}th number is: {}".format(turns, current_number))

if __name__ == "__main__":
    filename = "test.txt"
    arr = arrayise(filename)
    arr = [int(x) for x in arr[0].split(',')]
    day15([0,3,6])
    day15([1,3,2])
    day15([2,1,3])
    day15([1,2,3])
    day15([2,3,1])
    day15([3,2,1])
    day15([3,1,2])
    print()
    print("Part 1:")
    day15([0,3,1,6,7,5])
    print()
    print("Part 2:")
    day15([0,3,1,6,7,5], turns=30000000)