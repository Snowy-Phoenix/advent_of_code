def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def is_adjacent(row, col, array):
    for i in {-1, 0, 1}:
        for j in {-1, 0, 1}:
            next_row = row + i
            next_col = col + j
            if (0 <= next_row < len(array)):
                if (0 <= next_col < len(array[next_row])):
                    if array[next_row][next_col].isdigit():
                        continue
                    elif array[next_row][next_col] == ".":
                        continue
                    return True
    return False

def get_adjacent_gear(row, col, array):
    for i in {-1, 0, 1}:
        for j in {-1, 0, 1}:
            next_row = row + i
            next_col = col + j
            if (0 <= next_row < len(array)):
                if (0 <= next_col < len(array[next_row])):
                    if array[next_row][next_col] == "*":
                        return (next_row, next_col)
    return None

def solve(array):
    digit_sum = 0
    gears = dict()
    for row, line in enumerate(array):
        number_is_adjacent = False
        n = 0
        curr_gears = set()
        for col, char in enumerate(line):
            if char.isdigit():
                n *= 10
                n += int(char)
                if (is_adjacent(row, col, array)):
                    number_is_adjacent = True
                gear = get_adjacent_gear(row, col, array)
                if gear != None:
                    curr_gears.add(gear)
            else:
                for g in curr_gears:
                    if g not in gears:
                        gears[g] = []
                    gears[g].append(n)
                curr_gears.clear()
                if number_is_adjacent:
                    print(n)
                    digit_sum += n
                    n = 0
                    number_is_adjacent = False
                else:
                    n = 0
        for g in curr_gears:
            if g not in gears:
                gears[g] = []
            gears[g].append(n)
        curr_gears.clear()
        if number_is_adjacent:
            print(n)
            digit_sum += n
            n = 0
            number_is_adjacent = False
        else:
            n = 0
    g_ratios = 0
    for g in gears:
        ratios = gears[g]
        if len(ratios) == 2:
            g_ratios += ratios[0] * ratios[1]
    print(digit_sum)
    print(g_ratios)


if __name__ == '__main__':
    filename = "input3.txt"
    arr = arrayise(filename)
    solve(arr)