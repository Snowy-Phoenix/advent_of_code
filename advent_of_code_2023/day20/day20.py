from collections import deque

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def solve(lines):
    broadcast = []
    modules = dict() # name : type, rules, memory
    cons = dict() # name, all high?
    for line in lines:
        name, rules = line.split(" -> ")
        rules = rules.split(", ")
        if name == "broadcaster":
            broadcast = rules
        if name[0] == '&':
            cons[name[1:]] = []
            modules[name[1:]] = (name[0], rules, dict()) # input name: high received?
        else:
            modules[name[1:]] = (name[0], rules, False)
    for m in modules:
        for r in modules[m][1]:
            if (r not in modules):
                continue
            if (modules[r][0] == '&'):
                modules[r][2][m] = False
    lows = 0
    highs = 0
    i = 0
    rx_low_received = False

    sv = 0
    ng = 0
    ft = 0
    jz = 0
    print(3803 * 3877 * 3889 * 3917)
    while i < 1000 or not rx_low_received:
        if (i == 1000):
            print("Part 1:", lows * highs, lows, highs)
        
        queue = deque()
        queue.append(('low', 'broadcaster'))
        while len(queue) > 0:
            node = queue.popleft()
            if (node[1] == 'rx' and node[0] == 'low'):
                print("Part 2:", i)
                rx_low_received = True
            # print(node)
            if (node[0] == 'high'):
                highs += 1
            else:
                lows += 1
            if (node[1] == 'broadcaster'):
                for m in broadcast:
                    queue.append(('low', m))
                continue
            
            if (node[1] not in modules):
                continue
            mod = modules[node[1]]

            pulse = 'high'
            if mod[0] == '%':
                if node[0] == 'high':
                    continue
                if mod[2]:
                    pulse = 'low'
                for m in mod[1]:
                    queue.append((pulse, m))
                modules[node[1]] = (mod[0], mod[1], not mod[2])
            else:
                pulse = 'low'
                for name in mod[2]:
                    if (not mod[2][name]):
                        pulse = 'high'
                        break
                for m in mod[1]:
                    queue.append((pulse, m))
            
            if (node[1] == 'sv'):
                if (pulse == 'high'):
                    print(node[1], i)
            if (node[1] == 'ng'):
                if (pulse == 'high'):
                    print(node[1], i)
            if (node[1] == 'ft'):
                if (pulse == 'high'):
                    print(node[1],i)
            if (node[1] == 'jz'):
                if (pulse == 'high'):
                    print(node[1],i)
            for r in mod[1]:
                if r not in modules:
                    continue
                if modules[r][0] == '&':
                    if pulse == 'high':
                        modules[r][2][node[1]] = True
                    else:
                        modules[r][2][node[1]] = False
        i += 1
            
        
if __name__ == '__main__':
    filename = "input20.txt"
    arr = arrayise(filename)
    solve(arr)