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


class Blueprint:
    def __init__(self, blueprint_id, ore, clay, obsidian, geode, max_turns):
        self.blueprint_id = blueprint_id
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode
        self.max_turns = max_turns
    def __repr__(self):
        return str((self.blueprint_id, self.ore, self.clay, self.obsidian, self.geode))

class Turn:
    def __init__(self, turn_number, ore_robots, ores, clay_robots, clay, obsidian_robots, obsidian, geode_robots, geodes, level=0):
        self.turn_number = turn_number
        self.ore_robots = ore_robots
        self.ores = ores
        self.clay_robots = clay_robots
        self.clay = clay
        self.obsidian_robots = obsidian_robots
        self.obsidian = obsidian
        self.geode_robots = geode_robots
        self.geodes = geodes
        self.level = level
    
    def get_turn_until_next_ore_robot(self, blueprint):
        if (self.ore_robots >= max(blueprint.ore, blueprint.clay, blueprint.obsidian[0], blueprint.geode[0])):
            return None
        difference = blueprint.ore - self.ores
        turns = 1
        if (difference > 0):
            turns += math.ceil(difference / self.ore_robots)
        return Turn(self.turn_number + turns, 
                    self.ore_robots + 1, 
                    self.ores + (self.ore_robots * turns) - blueprint.ore, 
                    self.clay_robots, 
                    self.clay + (self.clay_robots * turns), 
                    self.obsidian_robots, 
                    self.obsidian + (self.obsidian_robots * turns), 
                    self.geode_robots, 
                    self.geodes + (self.geode_robots * turns), 0)

    def get_turn_until_next_clay_robot(self, blueprint):
        difference = blueprint.clay - self.ores
        turns = 1
        if (difference > 0):
            turns += math.ceil(difference / self.ore_robots)
        return Turn(self.turn_number + turns, 
                    self.ore_robots, 
                    self.ores + (self.ore_robots * turns) - blueprint.clay, 
                    self.clay_robots + 1, 
                    self.clay + (self.clay_robots * turns), 
                    self.obsidian_robots,
                    self.obsidian + (self.obsidian_robots * turns), 
                    self.geode_robots, 
                    self.geodes + (self.geode_robots * turns), 1)

    def get_turn_until_next_obsidian_robot(self, blueprint):
        if (self.clay_robots == 0):
            return None
        difference_ore = blueprint.obsidian[0] - self.ores
        difference_clay = blueprint.obsidian[1] - self.clay
        turns = 1
        if (difference_ore > 0):
            turns += math.ceil(difference_ore / self.ore_robots)
        if (difference_clay > 0):
            turns = max(turns, 1 + math.ceil(difference_clay / self.clay_robots))
        return Turn(self.turn_number + turns, 
                    self.ore_robots, 
                    self.ores + (self.ore_robots * turns) - blueprint.obsidian[0], 
                    self.clay_robots, 
                    self.clay + (self.clay_robots * turns) - blueprint.obsidian[1], 
                    self.obsidian_robots + 1,
                    self.obsidian + (self.obsidian_robots * turns), 
                    self.geode_robots, 
                    self.geodes + (self.geode_robots * turns), 2)

    def get_turn_until_next_geode_robot(self, blueprint):
        if (self.obsidian_robots == 0):
            return None
        difference_ore = blueprint.geode[0] - self.ores
        difference_obsidian = blueprint.geode[1] - self.obsidian
        turns = 1
        if (difference_ore > 0):
            turns += math.ceil(difference_ore / self.ore_robots)
        if (difference_obsidian > 0):
            turns = max(turns, 1 + math.ceil(difference_obsidian / self.obsidian_robots))
        return Turn(self.turn_number + turns, 
                    self.ore_robots, 
                    self.ores + (self.ore_robots * turns) - blueprint.geode[0], 
                    self.clay_robots, 
                    self.clay + (self.clay_robots * turns), 
                    self.obsidian_robots,
                    self.obsidian + (self.obsidian_robots * turns) - blueprint.geode[1], 
                    self.geode_robots + 1, 
                    self.geodes + (self.geode_robots * turns), 2)

    def wait_until(self, turn_number):
        turns = turn_number - self.turn_number
        return Turn(self.turn_number + turns, 
                    self.ore_robots, 
                    self.ores + (self.ore_robots * turns), 
                    self.clay_robots, 
                    self.clay + (self.clay_robots * turns), 
                    self.obsidian_robots,
                    self.obsidian + (self.obsidian_robots * turns), 
                    self.geode_robots, 
                    self.geodes + (self.geode_robots * turns), self.level)

    def get_next_turns(self, blueprint, max_turns):
        turns = []
        # if (self.level == 0):
        #     if (self.ore_robots < max(blueprint.ore, blueprint.clay, blueprint.obsidian[0], blueprint.geode[0])):
        #         turns.append(self.get_turn_until_next_ore_robot(blueprint))
        #     turns.append(self.get_turn_until_next_clay_robot(blueprint))
        # elif self.level == 1:
        #     if (self.ore_robots < max(blueprint.ore, blueprint.clay, blueprint.obsidian[0], blueprint.geode[0])):
        #         turns.append(self.get_turn_until_next_ore_robot(blueprint))
        #         turns[-1].level = 1
        #     turns.append(self.get_turn_until_next_clay_robot(blueprint))
        #     turns.append(self.get_turn_until_next_obsidian_robot(blueprint))
        # else:
        #     turns.append(self.get_turn_until_next_obsidian_robot(blueprint))
        #     turns.append(self.get_turn_until_next_geode_robot(blueprint))
        
        if (self.turn_number == max_turns - 1):
            # second last minute. 
            # Our new robot cannot produce anything, so don't bother checking.
            turns.append(self.wait_until(max_turns))
            return turns
        if (self.ore_robots < max(blueprint.ore, blueprint.clay, blueprint.obsidian[0], blueprint.geode[0])):
            # Don't create more robots than necessary.
            turns.append(self.get_turn_until_next_ore_robot(blueprint))
        if (self.clay < blueprint.obsidian[1] * 1.2):
            # Make sure that we are not building more robots than necessary.
            turns.append(self.get_turn_until_next_clay_robot(blueprint))
        if (self.clay_robots and self.obsidian < blueprint.geode[1]):
            turns.append(self.get_turn_until_next_obsidian_robot(blueprint))
        if (self.obsidian_robots):
            turns.append(self.get_turn_until_next_geode_robot(blueprint))
        
        valid_turns = []
        for t in turns:
            if (t.turn_number <= max_turns):
                valid_turns.append(t)

        if len(valid_turns) == 0 and self.geode_robots:
            valid_turns.append(self.wait_until(max_turns))
        return valid_turns

    def __repr__(self):
        return str((self.turn_number, self.ore_robots, self.ores, self.clay_robots, self.clay, self.obsidian_robots, self.obsidian, self.geode_robots, self.geodes))

    def __hash__(self):
        return hash((self.ore_robots, self.ores, self.clay_robots, self.clay, self.obsidian_robots, self.obsidian, self.geode_robots))
    def __eq__(self, other):
        return (self.ore_robots, self.ores, self.clay_robots, self.clay, self.obsidian_robots, self.obsidian, self.geode_robots) == \
              (other.ore_robots, other.ores, other.clay_robots, other.clay, other.obsidian_robots, other.obsidian, other.geode_robots)

def simulate_best(blueprint, max_turns):
    states = deque() # (turn number, ore, clay, ob, geode, opened)
    start = Turn(0, 1, 0, 0, 0, 0, 0, 0, 0)
    states.append(start)
    max_geodes = 0
    max_geode_robots = 0
    max_obsidian_robots = 0
    curr_turn = 0
    best = None
    while (len(states) > 0):
        turn = states.pop()
        
        max_geode_robots = max(max_geode_robots, turn.geode_robots)
        max_obsidian_robots = max(max_obsidian_robots, turn.obsidian_robots)
        if turn.turn_number >= max_turns:
            if (max_geodes < turn.geodes):
                max_geodes = turn.geodes
                best = turn
        else:
            for t in turn.get_next_turns(blueprint, max_turns):
                states.append(t)
    if (best is None):
        return 0
    return max_geodes


def solve(arr):
    blueprints = []
    for line in arr:
        if line == '':
            continue
        tokens = line.split()
        blueprint_id = int(tokens[1].strip(':'))
        ore = int(tokens[6])
        clay = int(tokens[12])
        ob_ore = int(tokens[18])
        ob_clay = int(tokens[21])
        geode_ore = int(tokens[27])
        geode_ob = int(tokens[30])
        blueprints.append(Blueprint(blueprint_id, ore, clay, (ob_ore, ob_clay), (geode_ore, geode_ob), 24))
    best = dict()
    for b in blueprints:
        best[b.blueprint_id] = simulate_best(b, 24)
    quality = 0
    for b in best:
        quality += b * best[b]
    print("Part 1:", quality)
    part2 = simulate_best(blueprints[0], 32) * simulate_best(blueprints[1], 32)
    if len(blueprints) > 2:
        part *= simulate_best(blueprints[2], 32)
    print("Part 2:", part2)


if __name__ == '__main__':
    filename = "input19.txt"
    arr = arrayise(filename)
    solve(arr)
    