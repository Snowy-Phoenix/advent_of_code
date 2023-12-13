import re

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day10(array):
    diff_1 = 0
    diff_2 = 0
    diff_3 = 0
    reached_all_adapters = True
    for i in range(1, len(array)):
        difference = array[i] - array[i-1]
        if difference == 0:
            continue
        elif difference == 1:
            diff_1 += 1
        elif difference == 2:
            diff_2 += 1
        elif difference == 3:
            diff_3 += 1
        else:
            reached_all_adapters = False
            break
    print("Part 1:", diff_1 * diff_3)

    d = [0 for i in range(len(array))] # index, permutations
    d[len(array) - 1] = 1
    d[len(array) - 2] = 1
    d[len(array) - 3] = 1
    for i in range(len(array) - 4, -1, -1):
        d[i] = int(array[i + 1] - array[i] <= 3) * d[i + 1]
        d[i] += int(array[i + 2] - array[i] <= 3) * d[i + 2]
        d[i] += int(array[i + 3] - array[i] <= 3) * d[i + 3]
    print("Part 2:", d[0])
        


if __name__ == "__main__":
    filename = "input10.txt"
    arr = arrayise(filename)
    arr = [int(x) for x in arr]
    arr.append(0)
    arr.append(max(arr) + 3)
    arr = sorted(arr)
    day10(arr)