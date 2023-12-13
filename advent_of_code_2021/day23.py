import math
import re
import numpy as np
import copy
import itertools

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

class Burrow:
    def __init__(self, hallways, rooms):
        self.hallways = hallways
        self.rooms = rooms
        self.room_length = len(rooms[0])
        self.multiplier = {'A':1, 'B':10, 'C':100, 'D':1000}
        self.amphipod_numbers = ['A', 'B', 'C', 'D']
        self.room_destinations = {'A':0, 'B':1, 'C':2, 'D':3}
                
    def encode_as_tuple(self, hallways, rooms):
        encoding = []
        for hallway in hallways:
            encoding.append(hallway)
        for room in rooms:
            for tile in room:
                encoding.append(tile)
        return tuple(encoding)

    def occupy_rooms(self, state):
        cum_energy_before = 0
        cum_energy_after = 0
        while True:
            for room_number in range(4):
                cum_energy_after += self.occupy_room(state, room_number)
            if cum_energy_after == cum_energy_before:
                return cum_energy_after
            else:
                cum_energy_before = cum_energy_after

    def occupy_room(self, state, room_number):
        hallways = state[:len(self.hallways)]
        rooms = state[len(self.hallways):]
        room_i = self.room_length * room_number
        correct_amphipod = self.amphipod_numbers[room_number]
        multiplier = self.multiplier[correct_amphipod]
        energy_spent = 0
        steps = 1

        room_depth = 0
        for i in range(self.room_length):
            room_tile = rooms[room_i + i]
            if room_tile == '.':
                room_depth = i
                steps += 1
            elif room_tile != correct_amphipod:
                return 0
            else:
                continue
        room_i += room_depth

        energy_spent = 0
        left_i = room_number + 1
        right_i = room_number + 2
        left_unobstructed = True
        right_unobstructed = True
        while left_unobstructed or right_unobstructed:
            if left_unobstructed:
                left_amphipod = hallways[left_i]
                if left_amphipod == correct_amphipod:
                    energy_spent += steps * multiplier
                    if left_i == 0:
                        energy_spent -= multiplier
                    state[left_i] = '.'
                    state[len(hallways) + room_i] = correct_amphipod
                    room_i -= 1
                    steps -= 1 # We have filled the backmost vacant spot of the room.
                elif left_amphipod != '.':
                    left_unobstructed = False
                left_i -= 1
                if left_i < 0:
                    left_unobstructed = False

            if right_unobstructed:
                right_amphipod = hallways[right_i]
                if right_amphipod == correct_amphipod:
                    energy_spent += steps * multiplier
                    if right_i == len(hallways) - 1:
                        energy_spent -= multiplier
                    state[right_i] = '.'
                    state[len(hallways) + room_i] = correct_amphipod
                    room_i -= 1
                    steps -= 1 # We have filled the backmost vacant spot of the room.
                elif right_amphipod != '.':
                    right_unobstructed = False
                right_i += 1
                if right_i >= len(hallways):
                    right_unobstructed = False
            
            steps += 2
        return energy_spent

    def generate_finished(self):
        ls = []
        for _ in range(len(self.hallways)):
            ls.append(".")
        for _ in range(self.room_length):
            ls.append('A')
        for _ in range(self.room_length):
            ls.append('B')
        for _ in range(self.room_length):
            ls.append('C')
        for _ in range(self.room_length):
            ls.append('D')
        return tuple(ls)

    def step(self, state, energy=0):
        new_states = dict()
        previous_energy = energy
        hallways = state[:len(self.hallways)]
        rooms = state[len(self.hallways):]
        for room_i in range(0, len(rooms), self.room_length):
            curr_amphipod = rooms[room_i]
            # Get the amphipod and the current steps out of the room.
            steps_out_room = 1
            for i in range(self.room_length):
                curr_amphipod = rooms[room_i]
                if curr_amphipod == '.':
                    room_i += 1
                    steps_out_room += 1
            
            # The room is empty, so do nothing.
            if curr_amphipod == '.':
                continue
            # Check if the room is filled correctly.
            destination = self.room_destinations[curr_amphipod]
            if destination == room_i // self.room_length:
                is_proper = True
                for i in range(self.room_length - (room_i % self.room_length) - 1):
                    tile = rooms[room_i + i + 1]
                    if tile != curr_amphipod:
                        is_proper = False
                        break
                if is_proper:
                    continue
            multiplier = self.multiplier[curr_amphipod]
            energy_walking_out_of_room = multiplier * (steps_out_room + 1)
            energy_walking_through_hallways = 0
            
            left_unobstructed = True
            right_unobstructed = True
            left_i = (room_i // self.room_length) + 1
            right_i = left_i + 1
            while left_unobstructed or right_unobstructed:
                if left_unobstructed:
                    left_tile = hallways[left_i]
                    if left_tile == '.':
                        new_state = list(state)
                        new_state[left_i] = curr_amphipod
                        new_state[len(hallways) + room_i] = '.'
                        room_occupation_energy = self.occupy_rooms(new_state)
                        new_state = tuple(new_state)
                        total_energy_spent = previous_energy + room_occupation_energy + energy_walking_out_of_room + energy_walking_through_hallways
                        if left_i == 0:
                            total_energy_spent -= multiplier
                        if new_state in new_states:
                            new_states[new_state] = min(total_energy_spent, new_states[new_state])
                        else:
                            new_states[new_state] = total_energy_spent
                        left_i -= 1
                        if left_i < 0:
                            left_unobstructed = False
                    else:
                        left_unobstructed = False
                if right_unobstructed:
                    right_tile = hallways[right_i]
                    if right_tile == '.':
                        new_state = list(state)
                        new_state[right_i] = curr_amphipod
                        new_state[len(hallways) + room_i] = '.'
                        
                        room_occupation_energy = self.occupy_rooms(new_state)
                        total_energy_spent = previous_energy + room_occupation_energy + energy_walking_out_of_room + energy_walking_through_hallways
                        if right_i == len(hallways) - 1:
                            total_energy_spent -= multiplier
                        new_state = tuple(new_state)
                        if new_state in new_states:
                            new_states[new_state] = min(total_energy_spent, new_states[new_state])
                        else:
                            new_states[new_state] = total_energy_spent
                        right_i += 1
                        if right_i >= len(hallways):
                            right_unobstructed = False
                    else:
                        right_unobstructed = False
                energy_walking_through_hallways += 2 * multiplier
        return new_states

    def get_minimal_energy(self, show_solution=False):

        start_state = self.encode_as_tuple(self.hallways, self.rooms)

        finishing_state = self.generate_finished()
        visited_states = dict() # state, cost
        state_prev = dict() # state, its previous.
        state_prev[start_state] = None
        current_states = {start_state:0}
        

        while len(current_states) > 0:
            new_states = dict()
            for state in current_states:
                if state not in visited_states:
                    visited_states[state] = current_states[state]
                else:
                    visited_states[state] = min(visited_states[state], current_states[state])
                previous_energy = current_states[state]
                hallways = state[:len(self.hallways)]
                rooms = state[len(self.hallways):]
                for room_i in range(0, len(rooms), self.room_length):
                    curr_amphipod = rooms[room_i]

                    # Get the amphipod and the current steps out of the room.
                    steps_out_room = 1
                    for i in range(self.room_length):
                        curr_amphipod = rooms[room_i]
                        if curr_amphipod == '.':
                            room_i += 1
                            steps_out_room += 1
                    
                    # The room is empty, so do nothing.
                    if curr_amphipod == '.':
                        continue

                    # Check if the room is filled correctly.
                    destination = self.room_destinations[curr_amphipod]
                    if destination == room_i // self.room_length:
                        is_proper = True
                        for i in range(self.room_length - (room_i % self.room_length) - 1):
                            tile = rooms[room_i + i + 1]
                            if tile != curr_amphipod:
                                is_proper = False
                                break
                        if is_proper:
                            continue

                    multiplier = self.multiplier[curr_amphipod]
                    energy_walking_out_of_room = multiplier * (steps_out_room + 1)
                    energy_walking_through_hallways = 0
                    
                    left_unobstructed = True
                    right_unobstructed = True
                    left_i = (room_i // self.room_length) + 1
                    right_i = left_i + 1
                    while left_unobstructed or right_unobstructed:
                        if left_unobstructed:
                            left_tile = hallways[left_i]
                            if left_tile == '.':
                                new_state = list(state)
                                new_state[left_i] = curr_amphipod
                                new_state[len(hallways) + room_i] = '.'
                                room_occupation_energy = self.occupy_rooms(new_state)
                                new_state = tuple(new_state)

                                total_energy_spent = previous_energy + room_occupation_energy + energy_walking_out_of_room + energy_walking_through_hallways
                                if left_i == 0:
                                    # End of hallway. It took us 1 less step to get there.
                                    total_energy_spent -= multiplier
                                if new_state in new_states:
                                    if new_states[new_state] > total_energy_spent:
                                        new_states[new_state] = total_energy_spent
                                        state_prev[new_state] = state
                                else:
                                    new_states[new_state] = total_energy_spent
                                    state_prev[new_state] = state
                                
                                left_i -= 1
                                if left_i < 0:
                                    left_unobstructed = False
                            else:
                                left_unobstructed = False
                        if right_unobstructed:
                            right_tile = hallways[right_i]
                            if right_tile == '.':
                                new_state = list(state)
                                new_state[right_i] = curr_amphipod
                                new_state[len(hallways) + room_i] = '.'
                                
                                room_occupation_energy = self.occupy_rooms(new_state)
                                total_energy_spent = previous_energy + room_occupation_energy + energy_walking_out_of_room + energy_walking_through_hallways
                                if right_i == len(hallways) - 1:
                                    # End of hallway. It took us 1 less step to get there.
                                    total_energy_spent -= multiplier
                                new_state = tuple(new_state)

                                if new_state in new_states:
                                    if new_states[new_state] > total_energy_spent:
                                        new_states[new_state] = total_energy_spent
                                        state_prev[new_state] = state
                                else:
                                    new_states[new_state] = total_energy_spent
                                    state_prev[new_state] = state

                                right_i += 1
                                if right_i >= len(hallways):
                                    right_unobstructed = False
                            else:
                                right_unobstructed = False
                        energy_walking_through_hallways += 2 * multiplier
            current_states = new_states
            new_states = dict()
        if finishing_state not in visited_states:
            print("No solutions.")
            return -1
        if show_solution:
            self.print_solution(finishing_state, state_prev, visited_states)
        return visited_states[finishing_state]
    
    def print_solution(self, final_state, state_previouses, energies):
        states = []
        curr_state = final_state
        while curr_state != None:
            states.insert(0, curr_state)
            curr_state = state_previouses[curr_state]
        for state in states:
            self.print_state(state, energies[state])
    
    def print_state(self, state, energy):
        hallway = state[:7]
        rooms = state[7:]

        string = "Energy: {}\n".format(energy)
        string += "#############\n"

        string += "#"
        for i, c in enumerate(hallway):
            if i > 1 and i < len(hallway) - 1:
                string += '.'
            string += c
        string += "#\n"

        string += "###"
        for i in range(4):
            room_i = i * self.room_length
            string += rooms[room_i] + "#"
        string += "##\n"

        for i in range(1, self.room_length):
            string += "  #"
            for j in range(4):
                room_i = j * self.room_length + i
                string += rooms[room_i] + "#"
            string += "\n"
        
        string += "  #########\n"
        
        print(string)
        

def day23a(array, show_solution=False):
    hallways = ['.', '.', '.', '.', '.', '.', '.']
    rooms = [[], [], [], []]
    for i in range(2):
        room = 0    
        for c in array[2 + i]:
            if c.isalpha():
                rooms[room].append(c)
                room += 1
    burrow = Burrow(hallways, rooms)
    print("Part 1:", burrow.get_minimal_energy(show_solution))
    
def day23b(array, show_solution=False):
    hallways = ['.', '.', '.', '.', '.', '.', '.']
    rooms = [[], [], [], []]
    layer2 = ['D', 'C', 'B', 'A']
    layer3 = ['D', 'B', 'A', 'C']
    room = 0
    for c in array[2]:
        if c.isalpha():
            rooms[room].append(c)
            room += 1
    for room, c in enumerate(layer2):
        if c.isalpha():
            rooms[room].append(c)
    for room, c in enumerate(layer3):
        if c.isalpha():
            rooms[room].append(c)
    room = 0
    for c in array[3]:
        if c.isalpha():
            rooms[room].append(c)
            room += 1
    burrow = Burrow(hallways, rooms)
    print("Part 2:", burrow.get_minimal_energy(show_solution))
    
if __name__ == "__main__":
    filename = "input23.txt"
    arr = arrayise(filename)
    day23a(arr, show_solution=False)
    day23b(arr, show_solution=False)