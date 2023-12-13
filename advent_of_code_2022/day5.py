def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip("\n"))
    return array

class Cargo:
    def __init__(self):
        self.stack = []
    
    def pop(self, i):
        return self.stack[i].pop()

    def push(self, i, c):
        while (i >= len(self.stack)):
            self.stack.append([])
        self.stack[i].append(c)
    
    def move_pop(self, n, from_i, to_i):
        for _ in range(n):
            if len(self.stack[from_i]) == 0:
                return
            self.push(to_i, self.pop(from_i))
    
    def move_block(self, n, from_i, to_i):
        from_stack = self.stack[from_i]
        for i in range(n):
            self.push(to_i, from_stack[len(from_stack) - n + i])
        for _ in range(n):
            from_stack.pop()

def parse_cargo(array):
    cargo = Cargo()
    for line in array:
        if line:
            i = 0
            while i < len(line):
                if (line[i] != ' '):
                    cargo.push(i // 4, line[i + 1])
                i += 4
        else:
            break
    for stack in cargo.stack:
        stack.reverse()
    return cargo

def part1(array):
    cargo = parse_cargo(array)
    i = 0
    while array[i].strip():
        i += 1
    i += 1
    for line_n in range(i, len(array)):
        move = array[line_n].strip().split()
        n = int(move[1])
        from_i = int(move[3]) - 1
        to_i = int(move[5]) - 1
        cargo.move_pop(n, from_i, to_i)
    top = ""
    for stack in cargo.stack:
        if stack:
            top += stack[-1]
    print("Part 1:", top)

def part2(array):
    cargo = parse_cargo(array)
    i = 0
    while array[i].strip():
        i += 1
    i += 1
    for line_n in range(i, len(array)):
        move = array[line_n].strip().split()
        n = int(move[1])
        from_i = int(move[3]) - 1
        to_i = int(move[5]) - 1
        cargo.move_block(n, from_i, to_i)
    top = ""
    for stack in cargo.stack:
        if stack:
            top += stack[-1]
    print("Part 2:", top)

def solve(array):
    part1(array)
    part2(array)

if __name__ == '__main__':
    filename = "input5.txt"
    arr = arrayise(filename)
    solve(arr)
