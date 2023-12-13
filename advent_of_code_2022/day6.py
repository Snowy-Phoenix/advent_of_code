from collections import deque

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def solve(array, distinct):
    text = array[0]
    queue = deque()
    for i, c in enumerate(text):
        if (len(queue) < distinct):
            queue.append(c)
        else:
            queue.popleft()
            queue.append(c)
            if (len(set(queue)) == distinct):
                return i + 1

if __name__ == '__main__':
    filename = "input6.txt"
    arr = arrayise(filename)
    print("Part 1:", solve(arr, 4))
    print("Part 2:", solve(arr, 14))
