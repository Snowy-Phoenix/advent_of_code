import math

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def triangular_num(n):
    return (n * (n+1)) // 2

def day7b(arr):
    raw_numbers = arr[0].split(',')
    numbers = []
    for i in raw_numbers:
        numbers.append(int(i))
    numbers = sorted(numbers)

    minimum = triangular_num(sum(numbers))

    for i in range(numbers[-1]):
        summation = 0
        for n in numbers:
            summation += triangular_num(abs(i - n))
        if (summation < minimum):
            minimum = summation
    return minimum

def day7a(arr):
    raw_numbers = arr[0].split(',')
    numbers = []
    for i in raw_numbers:
        numbers.append(int(i))
    numbers = sorted(numbers)

    minimum = sum(numbers)

    for i in range(numbers[-1]):
        summation = 0
        for n in numbers:
            summation += abs(i - n)
        if (summation < minimum):
            minimum = summation
    return minimum           

if __name__ == "__main__":
    filename = "input7.txt"
    arr = arrayise(filename)
    print(day7a(arr))
    print(day7b(arr))
