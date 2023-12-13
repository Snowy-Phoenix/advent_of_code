from collections import deque

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def solve(arr):
    pipe_map = []
    s_row = 0
    s_col = 0
    for row, line in enumerate(arr):
        pipe_map.append([])
        for col, c in enumerate(line):
            if c == 'S':
                s_row = row
                s_col = col
            pipe_map[-1].append(c)
    visited = dict()
    vectors = {'|': [(1,0), (-1,0)],
               '-': [(0,1), (0,-1)],
               'L': [(-1,0), (0,1)],
               'J': [(-1,0), (0,-1)],
               '7': [(1,0), (0,-1)],
               'F': [(1,0), (0,1)],
               '.': [],
               'S': [(1,0), (-1,0),(0,1), (0,-1)]}
    up = {'L', 'J'}
    down = {'F', '7'}
    up_and_down = {'|'}
    to_visit = deque()
    for v in vectors['S']:
        r = v[0] + s_row
        c = v[1] + s_col
        char = pipe_map[r][c]
        for v2 in vectors[char]:
            if (r + v2[0] == s_row and c + v2[1] == s_col):
                to_visit.append((r, c, 1))
                if (v2[0] == 1):
                    up.add('S')
                if (v2[0] == -1):
                    down.add('S')
    visited = set()
    visited.add((s_row, s_col))
    max_steps = 0
    while len(to_visit) > 0:
        node = to_visit.popleft()
        if (node[0], node[1]) in visited:
            continue
        visited.add((node[0], node[1]))
        max_steps = max(max_steps, node[2])
        char = pipe_map[node[0]][node[1]]
        for v in vectors[char]:
            to_visit.append((node[0] + v[0], node[1] + v[1], node[2] + 1))
    
    print(max_steps)
    in_loop = set()
    out_loop = set()
    for r, line in enumerate(pipe_map):
        outofloop = True
        last_up_or_down = ""
        for c, char in enumerate(line):
            if (r, c) in visited:
                if char in up_and_down:
                    last_up_or_down = ""
                    outofloop = not outofloop
                elif char in up:
                    if last_up_or_down == "up":
                        last_up_or_down = ""
                        outofloop = not outofloop
                    elif last_up_or_down == "down":
                        last_up_or_down = ""
                    else:
                        last_up_or_down = "up"
                        outofloop = not outofloop
                elif char in down:
                    if last_up_or_down == "up":
                        last_up_or_down = ""
                    elif last_up_or_down == "down":
                        last_up_or_down = ""
                        outofloop = not outofloop
                    else:
                        last_up_or_down = "down"
                        outofloop = not outofloop
            else:
                if outofloop:
                    out_loop.add((r,c))
                else:
                    in_loop.add((r,c))
    print(len(in_loop))




if __name__ == '__main__':
    filename = "input10.txt"
    arr = arrayise(filename)
    solve(arr)