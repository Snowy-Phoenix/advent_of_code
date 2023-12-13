def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array


def solve(array):
    subsets = 0
    overlaps = 0
    for pair in array:
        elf1, elf2 = pair.split(',')
        min1, max1 = elf1.split('-')
        min1 = int(min1)
        max1 = int(max1)
        min2, max2 = elf2.split('-')
        min2 = int(min2)
        max2 = int(max2)
        if min1 > min2:
            # keep min1 < min2 to make overlapping calculations easier
            min1, max1, min2, max2 = min2, max2, min1, max1
        if ((max1 >= max2) or
            (min2 == min1 and max2 >= max1)):
           subsets += 1
        if (min2 <= max1):
            overlaps += 1
    print("Part 1:", subsets)
    print("Part 2:", overlaps)


if __name__ == '__main__':
    filename = "input4.txt"
    arr = arrayise(filename)
    solve(arr)