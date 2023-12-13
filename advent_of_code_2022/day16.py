from collections import deque
from collections import defaultdict
import heapq
import copy
import math

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

class Valves:
    def __init__(self, flow):
        self.flow = flow
        self.to = []
    
    def append(self, to_valve):
        self.to.append(to_valve)

class ValvesOptimised:
    def __init__(self, flow):
        self.flow = flow
        self.to = dict()
    
    def add(self, to_valve, cost):
        self.to[to_valve] = cost

def create_optimised_valve(valves, valve):
    queue = deque()
    visited = set()
    queue.append((0, valve))
    optimised_valve = ValvesOptimised(valves[valve].flow)
    while len(queue) > 0:
        curr_valve = queue.popleft()
        if (curr_valve[1] in visited):
            continue
        else:
            visited.add(curr_valve[1])
        if curr_valve[0] != 0 and valves[curr_valve[1]].flow > 0:
            optimised_valve.add(curr_valve[1], curr_valve[0])
        for v in valves[curr_valve[1]].to:
            queue.append((curr_valve[0] + 1, v))
    return optimised_valve

def reduce_valves(valves, flow_valves):
    # Valves: dict(str, valve_obj)
    # Flow_valves: set(str)
    start_valve = 'AA'
    new_valves = dict()
    for flow_valve in flow_valves:
        new_valves[flow_valve] = create_optimised_valve(valves, flow_valve)
    new_valves[start_valve] = create_optimised_valve(valves, start_valve)
    return new_valves
        
def part1(optimised_valves, flow_valves):
    start_valve = 'AA'
    queue = deque() # Minutes left
    visited = set()
    max_pressure = 0
    max_minutes_left = 30
    queue.append((max_minutes_left, start_valve, set(), 0)) # Minutes, valve, opened, current_flow
    while len(queue) > 0:
        minutes_left, valve, opened_valves, total_flow = queue.popleft()
        max_pressure = max(total_flow, max_pressure)
        sorted_open = list(opened_valves)
        sorted_open.sort()
        if (minutes_left == 21 and valve == 'JJ'):
            print(total_flow)
        if (valve, tuple(sorted_open)) in visited:
            continue
        else:
            visited.add((valve, tuple(sorted_open)))
        if flow_valves == opened_valves:
            continue
        elif minutes_left <= 0:
            continue
        else:
            for v in optimised_valves[valve].to:
                if v in opened_valves:
                    continue
                else:
                    cost = optimised_valves[valve].to[v]
                    minutes_opened = minutes_left - cost - 1
                    if minutes_opened <= 0:
                        continue
                    new_flow = total_flow + (optimised_valves[v].flow * minutes_opened)
                    new_opened_valves = copy.copy(opened_valves)
                    new_opened_valves.add(v)
                    queue.append((minutes_opened, v, new_opened_valves, new_flow))
    print("Part 1:", max_pressure)

def part2(optimised_valves, flow_valves):
    start_valve = 'AA'
    queue = deque() # Minutes left
    visited = set()
    max_pressure = 0
    path = None
    max_minutes_left = 26
    queue.append(((max_minutes_left, start_valve), (max_minutes_left, start_valve), set(), 0, None))
    # (your minutes, your valve), (elephant's minutes, elephant's valve), opened, current_flow, prev
    while len(queue) > 0:
        you, elephant, opened_valves, total_flow, prev = queue.popleft()
        if max_pressure < total_flow:
            max_pressure = max(total_flow, max_pressure)
            path = (you, elephant, opened_valves, total_flow, prev)
        sorted_open = list(opened_valves)
        sorted_open.sort()
        if (you[1], elephant[1], tuple(sorted_open)) in visited:
            continue
        else:
            visited.add((you[1], elephant[1], tuple(sorted_open)))
        if flow_valves == opened_valves:
            continue
        elif you[0] <= 0 and elephant[0] <= 0:
            continue
        elif you[0] >= elephant[0]:
            for v in optimised_valves[you[1]].to:
                if v in opened_valves:
                    continue
                else:
                    cost = optimised_valves[you[1]].to[v]
                    minutes_opened = you[0] - cost - 1
                    if minutes_opened <= 0:
                        continue
                    new_flow = total_flow + (optimised_valves[v].flow * minutes_opened)
                    new_opened_valves = copy.copy(opened_valves)
                    new_opened_valves.add(v)
                    new_you = (minutes_opened, v)
                    queue.append((new_you, elephant, new_opened_valves, new_flow, (you, elephant, opened_valves, total_flow, prev)))
        else:
            for v in optimised_valves[elephant[1]].to:
                if v in opened_valves:
                    continue
                else:
                    cost = optimised_valves[elephant[1]].to[v]
                    minutes_opened = elephant[0] - cost - 1
                    if minutes_opened <= 0:
                        continue
                    new_flow = total_flow + (optimised_valves[v].flow * minutes_opened)
                    new_opened_valves = copy.copy(opened_valves)
                    new_opened_valves.add(v)
                    new_elephant = (minutes_opened, v)
                    queue.append((you, new_elephant, new_opened_valves, new_flow, (you, elephant, opened_valves, total_flow, prev)))
    print("Part 2:", max_pressure)
    print(path)

def solve(arr):
    valves = dict()
    flow_valves = set()
    for line in arr:
        line = line.split()
        curr_valve = line[1]
        flow = int(line[4].strip("rate=;"))
        if flow > 0:
            flow_valves.add(curr_valve)
        if curr_valve not in valves:
            valves[curr_valve] = Valves(flow)
        next_valves = line[9:]
        for v in next_valves:
            v = v.strip(',')
            valves[curr_valve].append(v)
    
    optimised_valves = reduce_valves(valves, flow_valves)
    # for v in optimised_valves:
    #     print(v, optimised_valves[v].to)
    part1(optimised_valves, flow_valves)
    part2(optimised_valves, flow_valves)

if __name__ == '__main__':
    filename = "input16.txt"
    arr = arrayise(filename)
    solve(arr)
    