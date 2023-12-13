from collections import deque

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def solve_rushed(array):
    directories = dict()
    total_sum = 0
    directory = "/"
    summation = 0
    begin_sum = False
    for line in array:
        tokens = line.split()
        if tokens[0] == '$':
            if (begin_sum):
                directories[directory] = summation
                begin_sum = False
                summation = 0
            instruction = tokens[1]
            if (instruction == 'cd'):
                if tokens[2] == '/':
                    directory = "/"
                elif tokens[2] == '..':
                    d = directory[1:-1].split("/")
                    directory = "/"
                    for i in range(len(d) - 1):
                        directory += d[i]
                        directory += "/"
                else:
                    directory += tokens[2]
                    directory += "/"
            elif (instruction == 'ls'):
                summation = 0
                begin_sum = True
        else:
            if (tokens[0] == "dir"):
                continue
            else:
                summation += int(tokens[0])
    directories[directory] = summation

    for path in directories:
        if (path == '/'):
            continue
        directory = "/"
        d = path[1:-1].split("/")
        for i in range(len(d)):
            directories[directory] += directories[path]
            # print("Add", directories[path], 'to', directory)
            directory += d[i]
            directory += "/"
    total_sum = 0
    for path in directories:
        if directories[path] < 100000:
            total_sum += directories[path]
    print("Part 1:", total_sum)



    total_space = 70000000
    unused_space = 30000000
    space_left = total_space - directories['/']
    space_required = unused_space - space_left
    # print("Total space used:", directories['/'])
    # print("Space left:", space_left)
    # print("free requirements:", space_required)
    min_dir = 1<<31
    for path in directories:
        if directories[path] >= space_required:
            min_dir = min(directories[path], min_dir)
            # print(directories[path], path)
    print(min_dir)


def solve(array):
    directory_sizes = dict() # Path, size
    i = 0
    path = ""
    while i < len(array):
        line = array[i]
        tokens = line.split()
        if tokens[1] == 'ls':
            j = i + 1
            size = 0
            while j < len(array):
                line = array[j]
                tokens = line.split()
                if tokens[0] == '$':
                    break
                elif tokens[0] == 'dir':
                    pass
                else:
                    size += int(tokens[0])
                j += 1
            i = j
            directory_sizes[path] = size            
        elif tokens[1] == 'cd':
            if tokens[2] == '/':
                path = ''
            elif tokens[2] == '..':
                path = path[:path[:-1].rfind('/')]
            else:
                path += tokens[2]
            path += '/'
            i += 1
        else:
            print("Invalid instruction", line)
            i += 1
    
    for path in directory_sizes:
        curr_size = directory_sizes[path]
        while path != "/":
            path = path[:path[:-1].rfind("/")]
            path += "/"
            directory_sizes[path] += curr_size

    summation = 0
    for n in directory_sizes.values():
        if (n < 100000):
            summation += n
    print(directory_sizes)
    print("Part 1:", summation)

    total_space = 70000000
    min_unused_space = 30000000
    unused_space = total_space - directory_sizes['/']
    size_required = min_unused_space - unused_space

    min_size = total_space
    for n in directory_sizes.values():
        if (n >= size_required):
            min_size = min(min_size, n)
    print("Part 2:", min_size)


if __name__ == '__main__':
    filename = "input7.txt"
    arr = arrayise(filename)
    # solve_rushed(arr)
    solve(arr)
