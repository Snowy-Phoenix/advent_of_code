import math
import re
import numpy as np
import copy
import itertools
import time

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def get_cube_params(line):
    command, cube = line.split(' ')
    x_coords, y_coords, z_coords = cube.split(',')
    xmin, xmax = x_coords.split('..')
    xmin = int(xmin[2:])
    xmax = int(xmax)
    ymin, ymax = y_coords.split('..')
    ymin = int(ymin[2:])
    ymax = int(ymax)
    zmin, zmax = z_coords.split('..')
    zmin = int(zmin[2:])
    zmax = int(zmax)
    return (command, xmin, xmax, ymin, ymax, zmin, zmax)

def day22a(array):
    on_cubes = set() # Tuple x, y, z
    for line in array:
        command, xmin, xmax, ymin, ymax, zmin, zmax = get_cube_params(line)
        if xmin < -50 or 50 < xmax:
            continue
        if ymin < -50 or 50 < ymax:
            continue
        if zmin < -50 or 50 < zmax:
            continue
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                for z in range(zmin, zmax + 1):
                    if command == "on":
                        on_cubes.add((x, y, z))
                    else:
                        if (x, y, z) in on_cubes:
                            on_cubes.remove((x, y, z))
    print("Part 1:", len(on_cubes))
        
def day22b(array):
    instructions = []
    for line in array:
        command, xmin, xmax, ymin, ymax, zmin, zmax = get_cube_params(line)
        instruction_line = Cube(command, xmin, xmax, ymin, ymax, zmin, zmax)
        instructions.append(instruction_line)
    
    cubes_in_reactor = []
    for reactor_cube in instructions:
        new_reactor_cubes = []
        for curr_cubes in cubes_in_reactor:
            new_reactor_cubes.extend(curr_cubes.subtract_cube(reactor_cube))
        cubes_in_reactor = new_reactor_cubes
        new_reactor_cubes = []
        cubes_in_reactor.append(reactor_cube)

    total_on = 0
    for cube in cubes_in_reactor:
        if cube.status == 'on':
            total_on += cube.volume
    
    print("Part 2:", total_on)
        
class Interval:

    def __init__(self, minp, maxp):
        self.minp = minp
        self.maxp = maxp
        self.length = abs(maxp - minp)
    
    def get_overlapping_points(self, interval):
        # Interval: --------------
        # Self Int:     -----------------
        min_overlap = -1
        max_overlap = -1
        is_min_overlapping = False
        has_overlap = False
        if self.minp <= interval.minp <= self.maxp:
            #       ----------
            # ------------
            is_min_overlapping = True
            min_overlap = interval.minp
            max_overlap = self.maxp
            has_overlap = True

        if self.minp <= interval.maxp <= self.maxp:
            if is_min_overlapping:
                #    -----
                # -----------
                max_overlap = interval.maxp
                return Interval(min_overlap, max_overlap)
            else:
                # ---------
                #      ----------
                min_overlap = self.minp
                max_overlap = interval.maxp
                return Interval(min_overlap, max_overlap)

        if interval.minp <= self.minp <= interval.maxp:
            # ------------
            #     -----
            return Interval(self.minp, self.maxp)
        
        if not has_overlap:
            return None
        else:
            return Interval(min_overlap, max_overlap)
    
    def subtract_interval(self, interval):
        """
        Gets the interval(s) where self is subtracted by the other interval.
        If the interval completely overlaps self, then an empty list is returned.
        """
        overlapped_interval = self.get_overlapping_points(interval)
        if overlapped_interval == None:
            return [self]
        
        intervals = []
        overlapped_at_min = False
        if overlapped_interval.minp == self.minp:
            intervals.append(Interval(overlapped_interval.maxp + 1, self.maxp))
            overlapped_at_min = True
        if overlapped_interval.maxp == self.maxp:
            if overlapped_at_min:
                # The overlapping region is equal to self.
                return []
            else:
                intervals.append(Interval(self.minp, overlapped_interval.minp - 1))
        if overlapped_interval.minp != self.minp and overlapped_interval.maxp != self.maxp:
            intervals.append(Interval(self.minp, overlapped_interval.minp - 1))
            intervals.append(Interval(overlapped_interval.maxp + 1, self.maxp))
        return intervals
    
    def __repr__(self):
        return str((self.minp, self.maxp))

class Cube:
    def __init__(self, status, minx, maxx, miny, maxy, minz, maxz):
        assert minx <= maxx
        assert miny <= maxy
        assert minz <= maxz
        self.status = status
        self.x = Interval(minx, maxx)
        self.y = Interval(miny, maxy)
        self.z = Interval(minz, maxz)
        self.volume = (maxx + 1 - minx) * (maxy + 1 - miny) * (maxz + 1 - minz)
    
    def get_overlapping_cube(self, cube):

        overlapx = self.x.get_overlapping_points(cube.x)
        overlapy = self.y.get_overlapping_points(cube.y)
        overlapz = self.z.get_overlapping_points(cube.z)
        if overlapx == None or overlapy == None or overlapz == None:
            return None
        
        return Cube(self.status, overlapx.minp, overlapx.maxp, overlapy.minp, overlapy.maxp, overlapz.minp, overlapz.maxp)
    
    def subtract_cube(self, cube):
        """Subtract the overlapping region of self and cube from self. 
        Returns a list of cubes that fill the unsubtracted part of self."""
        overlapping_cube = self.get_overlapping_cube(cube)
        if overlapping_cube == None:
            return [self]

        intervalx = self.x.subtract_interval(overlapping_cube.x)
        intervaly = self.y.subtract_interval(overlapping_cube.y)
        intervalz = self.z.subtract_interval(overlapping_cube.z)

        new_cubes = []
        for x in intervalx:
            new_cubes.append(Cube(self.status, x.minp, x.maxp, 
                                  self.y.minp, self.y.maxp, 
                                  self.z.minp, self.z.maxp))
        for y in intervaly:
            new_cubes.append(Cube(self.status, overlapping_cube.x.minp, overlapping_cube.x.maxp, 
                                  y.minp, y.maxp, 
                                  self.z.minp, self.z.maxp))
        for z in intervalz:
            new_cubes.append(Cube(self.status, overlapping_cube.x.minp, overlapping_cube.x.maxp, 
                                  overlapping_cube.y.minp, overlapping_cube.y.maxp, 
                                  z.minp, z.maxp))
        return new_cubes
    
    def __repr__(self):
        return str((self.x, self.y, self.z))
    

if __name__ == "__main__":
    filename = "input22.txt"
    arr = arrayise(filename)
    day22a(arr)
    day22b(arr)