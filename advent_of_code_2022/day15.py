from collections import deque
from collections import defaultdict
import math

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def get_sensor_ranges(sensors, y):
    ranges = dict()
    for s in sensors:
        difference = sensors[s] - abs(s[1] - y)
        if (difference >= 0):
            ranges[s] = (s[0] - difference, s[0] + difference)
    return ranges

def count_not_distress(intervals):
    positions = 0
    if len(intervals) == 0:
        return 0
    max_interval = intervals[0][0]
    min_interval = intervals[0][0]
    for i in intervals:
        if i[1] > max_interval:
            positions += (i[1] - i[0] + 1)
            # print(i, positions, min_interval, max_interval)
            if (i[0] < max_interval):
                positions -= max_interval - i[0]
                # print(i[0] - max_interval)
        max_interval = max(i[1] + 1, max_interval)
        min_interval = max(i[0], min_interval)
    return positions

def get_distress_signal(intervals, max_xy):
    if len(intervals) == 0:
        return 0
    elif intervals[0][0] > 0:
        return 0
    max_interval = 0
    for i in intervals:
        if i[0] > max_interval + 1:
            return max_interval + 1
        else:
            max_interval = max(max_interval, i[1])
    return -1

def solve1(arr):
    sensors = dict()
    beacons = set()
    minx = 1 << 31
    maxx = 0
    for line in arr:
        line = line.split()
        sensorx = int(line[2].strip('x=,'))
        minx = min(minx, sensorx)
        maxx = max(maxx, sensorx)
        sensory = int(line[3].strip('y=:'))
        beaconx = int(line[8].strip('x=,'))
        beacony = int(line[9].strip('y='))
        sensors[(sensorx, sensory)] = abs(sensorx - beaconx) + abs(sensory - beacony)
        beacons.add((beaconx, beacony))
    y_pos = 2000000
    intervals = get_sensor_ranges(sensors, y_pos)
    # print(intervals)
    intervals = list(intervals.values())
    intervals.sort()
    # intervals = get_x_min_max_intervals(sensors, ranges)
    # intervals.sort()
    # print(intervals)
    positions = count_not_distress(intervals)
    
    for s in sensors:
        if s[1] == y_pos:
            positions -= 1
    for b in beacons:
        if b[1] == y_pos:
            positions -= 1
    print("Part 1:", positions)
    max_xy = 4000000
    for y in range(max_xy):
        intervals = get_sensor_ranges(sensors, y)
        intervals = list(intervals.values())
        intervals.sort()
        position = get_distress_signal(intervals, max_xy)
        if position != -1:
            print("Part 2:", position * 4000000 + y)
            return


if __name__ == '__main__':
    filename = "input15.txt"
    arr = arrayise(filename)
    solve1(arr)
    