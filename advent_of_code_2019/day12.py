import math
import re
import numpy as np
import itertools


def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.velx = 0
        self.vely = 0
        self.velz = 0
    
    def __str__(self) -> str:
        string = "pos: <x={}, y={}, z={}>\n".format(self.x, self.y, self.z)
        string += "vel: <x={}, y={}, z={}>".format(self.velx, self.vely, self.velz)
        return string
    
    def __repr__(self) -> str:
        string = "{{pos:[{}, {}, {}], ".format(self.x, self.y, self.z)
        string += "vel:[{}, {}, {}]}}".format(self.velx, self.vely, self.velz)
        return string
    
    def __eq__(self, other) -> bool:
        result_pos = self.x == other.x and self.y == other.y and self.z == other.z
        # result_vel = self.velx == other.velx and self.vely == other.vely and self.velz == other.velz
        return  result_pos
    
    def get_total_energy(self):
        potential_energy = abs(self.x) + abs(self.y) + abs(self.z)
        kinetic_energy = abs(self.velx) + abs(self.vely) + abs(self.velz)
        return potential_energy * kinetic_energy

    def apply_velocity(self):
        self.x += self.velx
        self.y += self.vely
        self.z += self.velz
    
    def apply_gravity(self, moon):
        if isinstance(moon, self.__class__):
            if self.x < moon.x:
                self.velx += 1
            elif self.x > moon.x:
                self.velx -= 1

            if self.y < moon.y:
                self.vely += 1
            elif self.y > moon.y:
                self.vely -= 1

            if self.z < moon.z:
                self.velz += 1
            elif self.z > moon.z:
                self.velz -= 1
        else:
            raise TypeError

class MoonSystem:

    def __init__(self, moons):
        self.moons = moons
        self.tracked_moon = None
        self.tracked_moon_x = []
        self.tracked_moon_y = []
        self.tracked_moon_z = []
        self.tracked_moon_velx = []
        self.tracked_moon_vely = []
        self.tracked_moon_velz = []
        

    def tick_system(self):
        for i in range(len(self.moons)):
            moon1 = self.moons[i]
            for j in range(i + 1, len(self.moons)):
                moon2 = self.moons[j]
                moon1.apply_gravity(moon2)
                moon2.apply_gravity(moon1)
        
        for moon in self.moons:
            moon.apply_velocity()
    
    def simulate(self, steps=1):
        for i in range(steps):
            self.tick_system()
            if self.tracked_moon != None:
                self.tracked_moon_x.append(self.tracked_moon.x)
                self.tracked_moon_y.append(self.tracked_moon.y)
                self.tracked_moon_z.append(self.tracked_moon.z)
                self.tracked_moon_velx.append(self.tracked_moon.velx)
                self.tracked_moon_vely.append(self.tracked_moon.vely)
                self.tracked_moon_velz.append(self.tracked_moon.velz)
    
    def get_total_energy(self):
        total_energy = 0
        for moon in self.moons:
            total_energy += moon.get_total_energy()
        return total_energy

    def track_moon(self, moon):
        self.tracked_moon = moon

    def simulate_until_repeat(self):
        beginning_state_x = []
        beginning_state_y = []
        beginning_state_z = []
        x_cycle = -1
        y_cycle = -1
        z_cycle = -1
        for moon in self.moons:
            beginning_state_x.append((moon.x, moon.velx))
            beginning_state_y.append((moon.y, moon.vely))
            beginning_state_z.append((moon.z, moon.velz))
        steps = 1
        all_equal_x = False
        while True:
            self.simulate()
            all_equal_x = True
            all_equal_y = True
            all_equal_z = True
            for i in range(len(self.moons)):
                moon = self.moons[i]
                if x_cycle == -1 and (moon.x, moon.velx) != beginning_state_x[i]:
                    all_equal_x = False
                if y_cycle == -1 and (moon.y, moon.vely) != beginning_state_y[i]:
                    all_equal_y = False
                if z_cycle == -1 and (moon.z, moon.velz) != beginning_state_z[i]:
                    all_equal_z = False

            if all_equal_x and x_cycle == -1:
                x_cycle = steps
            if all_equal_y and y_cycle == -1:
                y_cycle = steps
            if all_equal_z and z_cycle == -1:
                z_cycle = steps
            if x_cycle != -1 and y_cycle != -1 and z_cycle != -1:
                return x_cycle, y_cycle, z_cycle
            steps += 1

    
    def __repr__(self) -> str:
        return str(self.moons)

def day12a(array):
    moons = []
    for line in array:
        line = line[1:-1]
        x,y,z = line.split(', ')
        x = int(x.split('=')[1])
        y = int(y.split('=')[1])
        z = int(z.split('=')[1])
        moons.append(Moon(x, y, z))
    moon_system = MoonSystem(moons)
    moon_system.simulate(1000)
    print("Part 1:", moon_system.get_total_energy())
    
def day12b(array):
    moons = []
    for line in array:
        line = line[1:-1]
        x,y,z = line.split(', ')
        x = int(x.split('=')[1])
        y = int(y.split('=')[1])
        z = int(z.split('=')[1])
        moons.append(Moon(x, y, z))
    moon_system = MoonSystem(moons)
    steps = moon_system.simulate_until_repeat()
    print("Part 2:", get_lcm(steps))
    print(steps)

def get_lcm(steps):
    x = steps[0]
    y = steps[1]
    z = steps[2]
    final_number = (x * y) // math.gcd(x, y)
    final_number = (final_number * z) // math.gcd(final_number, z)
    return final_number

if __name__ == "__main__":
    filename = "input12.txt"
    arr = arrayise(filename)

    day12a(arr)
    day12b(arr)
    

