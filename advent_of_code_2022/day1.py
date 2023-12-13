def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def solve(array):
    maximums = []
    elf_sum = 0
    for n in array:
        if n == '':
            maximums.append(elf_sum)
            elf_sum = 0
        else:
            elf_sum += int(n)
    maximums.sort(reverse=True)
    print("Part 1:", max(maximums))
    print("Part 2:", maximums[0] + maximums[1] + maximums[2])


if __name__ == '__main__':
    filename = "input1.txt"
    arr = arrayise(filename)
    solve(arr)