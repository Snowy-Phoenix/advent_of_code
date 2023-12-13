def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day5(array):
    highest_id = 0
    lowest_id = 2**31
    seats = set()
    for line in array:
        row = 0
        col = 0
        for c in line:
            if c == 'F':
                row = row << 1
            elif c == 'B':
                row = (row << 1) + 1
            elif c == 'R':
                col = (col << 1) + 1
            elif c == 'L':
                col = col << 1
        seat_id = row * 8 + col
        if (seat_id > highest_id):
            highest_id = seat_id
        elif (seat_id < lowest_id):
            lowest_id = seat_id
        seats.add(seat_id)
    print("Part 1:", highest_id)
    for i in range(lowest_id, highest_id):
        if i not in seats:
            print("Part 2:", i)
            return

if __name__ == "__main__":
    filename = "input5.txt"
    arr = arrayise(filename)
    day5(arr)

    
