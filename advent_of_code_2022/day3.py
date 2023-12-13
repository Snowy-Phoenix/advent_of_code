def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def get_priority(item: str):
    if (item.islower()):
        return (ord(item) - ord('a')) + 1
    else:
        return (ord(item) - ord('A')) + 27

def part1(array):
    priority = 0
    for rucksack in array:
        i = 0
        j = len(rucksack) - 1
        compartment1 = set()
        compartment2 = set()
        while (i < j):
            item1 = rucksack[i]
            item2 = rucksack[j]
            compartment1.add(item1)
            compartment2.add(item2)
            i += 1
            j -= 1
        duplicates = compartment1.intersection(compartment2)
        for item in duplicates:
            priority += get_priority(item)
        compartment1.clear()
        compartment2.clear()
    print("Part 1:", priority)

def part2(array):
    priority = 0
    for i in range(0, len(array), 3):
        rucksack1 = set(array[i])
        rucksack2 = set(array[i + 1])
        rucksack3 = set(array[i + 2])
        badge = rucksack1.intersection(rucksack2.intersection(rucksack3))
        if len(badge) != 1:
            print("Bad input: line {}", i)
        else:
            priority += get_priority(badge.pop())
    print("Part 2:", priority)

def solve(array):
    part1(array)
    part2(array)


if __name__ == '__main__':
    filename = "input3.txt"
    arr = arrayise(filename)
    solve(arr)