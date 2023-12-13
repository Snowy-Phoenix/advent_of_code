import re

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def get_max_i(array):
    maximum = 0
    max_i = -1
    for i in range(len(array)):
        if array[i] > maximum:
            max_i = i
            maximum = array[i]
    return max_i

def solve_congruence(m1, r1, m2, r2):
    for i in range(m2):
        if ((m1 * i + r1) % m2 == r2):
            return (m1*m2, m1*i + r1)
    return None

def day13(array):
    time = int(array[0])
    raw_schedules = array[1].split(',')
    schedules = []
    original_indices = []
    for i in range(len(raw_schedules)):
        t = raw_schedules[i]
        if t != 'x':
            schedules.append(int(t))
            original_indices.append(i)
    shortest_wait = 2**31
    bus_id = 0
    for t in schedules:
        waiting_time = t - (time % t)
        if waiting_time < shortest_wait:
            shortest_wait = waiting_time
            bus_id = t

    print("Bus id: {}, Time to wait: {}".format(bus_id, shortest_wait))
    print("Part 1:", bus_id * shortest_wait)

    index = get_max_i(schedules)
    final_modulus = schedules[index]
    final_remainder = (final_modulus - original_indices[index]) % final_modulus
    schedules.pop(index)
    original_indices.pop(index)

    while (len(schedules) > 0):
        index = get_max_i(schedules)
        modulus = schedules[index]
        remainder = (modulus- original_indices[index]) % modulus
        schedules.pop(index)
        original_indices.pop(index)
        solution = solve_congruence(final_modulus, final_remainder, modulus, remainder)
        final_modulus = solution[0]
        final_remainder = solution[1]
    
    print("Part 2:", final_remainder)

if __name__ == "__main__":
    filename = "input13.txt"
    arr = arrayise(filename)
    day13(arr)