import math
import re
import numpy as np
import copy
import itertools
import heapq
import pickle

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

class ScannerBeacons:
    def __init__(self, number, threshold=12):
        self.number = number
        self.threshold = threshold
        self.beacons = set()
        self.scanners = set([(0,0,0)])
        self.rotation_mappings = {
                        ('x', 'y', 'z'), ('x', '-z', 'y'), ('x', '-y', '-z'), ('x', 'z', '-y'),
                        ('y', '-x', 'z'), ('y', 'z', 'x'), ('y', 'x', '-z'), ('y', '-z', '-x'),
                        ('z', 'x', 'y'), ('z', 'y', '-x'), ('z', '-x', '-y'), ('z', '-y', 'x'),
                        ('-x', '-y', 'z'), ('-x', 'z', 'y'), ('-x', 'y', '-z'), ('-x', '-z', '-y'),
                        ('-y', 'x', 'z'), ('-y', 'z', '-x'), ('-y', '-x', '-z'), ('-y', '-z', 'x'),
                        ('-z', 'y', 'x'), ('-z', 'x', '-y'), ('-z', '-y', '-x'), ('-z', '-x', '-y')
                        }
    
    def add_beacon(self, beacon):
        self.beacons.add(beacon)

    def merge(self, scanner):
        # If the self and sensor has more than 12 common beacons, merge the sensors to self.
        for beacon1 in scanner.beacons:
            for beacon2 in self.beacons:
                translation_vector1 = []
                translation_vector2 = []
                for i in range(3):
                    translation_vector1.append(-beacon1[i])
                    translation_vector2.append(-beacon2[i])
                translated_points1 = translate_points(scanner.beacons, translation_vector1)
                translated_points2 = translate_points(self.beacons, translation_vector2)
                for rotation in self.rotation_mappings:
                    rotated_points = rotate_points(translated_points1, rotation)
                    common_points = translated_points2.intersection(rotated_points)
                    if len(common_points) >= self.threshold:

                        scanner_coords = translate_points([(0,0,0)], translation_vector1)
                        scanner_coords = rotate_points([scanner_coords.pop()], rotation)
                        scanner_coords = translate_points([scanner_coords.pop()], translation_vector2, sign=-1).pop()

                        rotated_scanners = rotate_points(scanner.scanners, rotation)

                        self.merge_scanners(rotated_scanners, scanner_coords)
                        new_points = rotate_points(scanner.beacons, rotation)
                        new_points = translate_points(new_points, scanner_coords)
                        for p in new_points:
                            self.beacons.add(p)
                        return True
        return False
    
    def merge_scanners(self, scanners, base_coordinates):
        other_points = list(scanners)
        translated_points = set()
        for i in range(len(other_points)):
            p = other_points[i]
            translated_p = translate_point(p, base_coordinates)
            translated_points.add(translated_p)
        self.scanners = self.scanners.union(translated_points)
            
    
    def __lt__(self, other):
        return len(self.beacons) < len(other.beacons)
    def __gt__(self, other):
        return len(self.beacons) > len(other.beacons)

def translate_point(point, vector):
    new_point = []
    for i in range(3):
        new_point.append(point[i] + vector[i])
    return tuple(new_point)

def translate_points(points, vector, sign=1):
    new_points = set()
    for p in points:
        new_point = []
        for i in range(3):
            new_point.append(p[i] + (sign * vector[i]))
        new_points.add(tuple(new_point))
    return new_points

def rotate_points(points, rotation):
    x_i = -1
    y_i = -1
    z_i = -1
    xsign = 1
    ysign = 1
    zsign = 1
    for i in range(len(rotation)):
        axis = rotation[i]
        atom = axis[-1]
        sign = 1
        if len(axis) == 2:
            sign = -1
        if atom == 'x':
            x_i = i
            xsign = sign
        elif atom == 'y':
            y_i = i
            ysign = sign
        else:
            z_i = i
            zsign = sign
    
    new_points = set()
    for p in points:
        new_points.add((xsign * p[x_i], ysign * p[y_i], zsign * p[z_i]))
    return new_points 

def get_largest_distance(coordinates):
    ls = list(coordinates)
    maximum = 0
    for i in range(len(ls)):
        for j in range(i + 1, len(ls)):
            c1 = ls[i]
            c2 = ls[j]
            maximum = max(maximum, abs(c1[0]-c2[0]) + abs(c1[1]-c2[1]) + abs(c1[2]-c2[2]))
    return maximum

def day19(array):
    scanners = []
    current_scanner = None
    for line in array:
        if line == '':
            continue
        is_header = re.fullmatch("--- scanner (\d+) ---", line)
        if is_header:
            current_scanner = ScannerBeacons(int(is_header.group(1)))
            scanners.append(current_scanner)
        else:
            coordinates = tuple(int(x) for x in line.split(','))
            current_scanner.add_beacon(coordinates)

    scanners = sorted(scanners)
    while len(scanners) > 1:
        curr_scanner = scanners.pop(0)
        merged = False
        for i in range(len(scanners)):
            other_scanner = scanners[i]
            merged = curr_scanner.merge(other_scanner)
            if merged:
                scanners.pop(i)
                scanners.append(curr_scanner)
                scanners = sorted(scanners)
                # print("Merged, {} left to merge".format(len(scanners)))
                break
        if not merged:
            print("Unable to merge.")
            break

    print("Part 1:", len(scanners[0].beacons))
    print("Part 2:", get_largest_distance(scanners[0].scanners))
    # with open("test.pkl", "wb") as output:
    #     pickle.dump(scanners[0], output, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    filename = "input19.txt"
    arr = arrayise(filename)
    day19(arr)
    # with open("test.pkl", "rb") as inp:
    #     scanner = pickle.load(inp)
    #     print("Get largest distance:", get_largest_distance(scanner.scanners))
    #     print(scanner.scanners)
    
