
def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def solve(array):
    time = # Puzzle input here
    distance = # Puzzle input here
    final = 1
    for i, t in enumerate(time):
        d = distance[i]
        count = 0
        for s in range(t):
            total_distance = (t - s) * (s)
            if total_distance > d:
                count += 1
        final *= count
    print(final)
    t = # Puzzle part 2 input here
    distance = # Puzzle part 2 input here
    count = 0
    for i in range(t):
        if (t - i) * (i) > distance:
            count += 1
    print(count)

if __name__ == '__main__':
    filename = "input6.txt"
    arr = arrayise(filename)
    solve(arr)