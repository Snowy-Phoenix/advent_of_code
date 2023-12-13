import re

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def get2(array, sum):
    numbers = set(array)  
    for n in numbers:
        if sum - n in numbers:
            return (sum - n, n)
    return None

def get_first_number_without_property(array, x):
    for upper in range(x, len(array)):
        n = array[upper]
        lower = upper - x
        if (get2(array[lower:upper], n)) == None:
            return n

def get_contiguous_sum(array, x):
    i = 0
    j = 1
    summation = array[0]
    while (j <= len(array)):
        if (summation == x):
            return (i, j)
        elif summation < x:
            summation += array[j]
            j += 1
        else:
            summation -= array[i]
            i += 1
    return None

def get_min_max(array, ranges):
    maximum = 0
    minimum = 2**31
    for i in array[ranges[0]:ranges[1]]:
        if i > maximum:
            maximum = i
        if i < minimum:
            minimum = i
    return (minimum, maximum)


def day9(array, x):
    magic_number = get_first_number_without_property(array, x)
    print("Part 1:", magic_number)
    
    contiguous_sum_range = get_contiguous_sum(array, magic_number)
    minimum, maximum = get_min_max(array, contiguous_sum_range)
    print("Part 2:", minimum + maximum)
    
if __name__ == "__main__":
    filename = "input9.txt"
    arr = arrayise(filename)
    arr = [int(x) for x in arr]
    day9(arr, 25)