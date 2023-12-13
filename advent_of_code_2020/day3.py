from os import cpu_count


def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day3(array, rows_per_step, cols_per_step):
    trees = 0
    row = 0
    col = 0
    while (row < len(array)):
        if array[row][col] == '#':
            trees += 1
        row += rows_per_step
        col = (col + cols_per_step) % len(array[0])
    return trees

if __name__ == "__main__":
    filename = "input3.txt"
    arr = arrayise(filename)
    print(day3(arr, 1, 3))

    print(day3(arr, 1, 1) * day3(arr, 1, 3) * day3(arr, 1, 5) * day3(arr, 1, 7) * day3(arr, 2, 1))
    
