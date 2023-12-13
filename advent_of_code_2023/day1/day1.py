def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def solve(array):
    sum = 0
    for line in array:
        first_digit = -1
        last_digit = 0

        while len(line) > 0:
            c = line[0]
            if c.isdigit():
                if first_digit == -1:
                    first_digit = int(c)
                last_digit = int(c)
            elif line.startswith("one"):
                if first_digit == -1:
                    first_digit = 1
                last_digit = 1
            elif line.startswith("two"):
                if first_digit == -1:
                    first_digit = 2
                last_digit = 2
            elif line.startswith("three"):
                if first_digit == -1:
                    first_digit = 3
                last_digit = 3
            elif line.startswith("four"):
                if first_digit == -1:
                    first_digit = 4
                last_digit = 4
            elif line.startswith("five"):
                if first_digit == -1:
                    first_digit = 5
                last_digit = 5
            elif line.startswith("six"):
                if first_digit == -1:
                    first_digit = 6
                last_digit = 6
            elif line.startswith("seven"):
                if first_digit == -1:
                    first_digit = 7
                last_digit = 7
            elif line.startswith("eight"):
                if first_digit == -1:
                    first_digit = 8
                last_digit = 8
            elif line.startswith("nine"):
                if first_digit == -1:
                    first_digit = 9
                last_digit = 9
            line = line[1:]
        sum += first_digit * 10 + last_digit
    print(sum)


if __name__ == '__main__':
    filename = "input1.txt"
    arr = arrayise(filename)
    solve(arr)