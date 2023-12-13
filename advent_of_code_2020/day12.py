import re

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day12a(array):
    DIRECTIONS = ['E', 'S', 'W', "N"]
    ship_direction = 0
    x = 0
    y = 0
    for line in array:
        direction = line[0]
        value = int(line[1:])
        if direction == 'F':
            direction = DIRECTIONS[ship_direction]
        if direction == 'R':
            ship_direction = (ship_direction + (value // 90)) % 4
        elif direction == 'L':
            ship_direction = (ship_direction - (value // 90)) % 4
        elif direction == 'N':
            y += value
        elif direction == 'E':
            x += value
        elif direction == 'S':
            y -= value
        elif direction == 'W':
            x -= value
    print("Part 1:", abs(x) + abs(y))

def rotate_waypoint(direction, value, waypoint_x, waypoint_y):
    if direction == "L":
        value = 360 - value
    rotation = (value // 90) % 4
    if rotation == 0:
        return (waypoint_x, waypoint_x)
    elif rotation == 1:
        return (waypoint_y, -waypoint_x)
    elif rotation == 2:
        return (-waypoint_x, -waypoint_y)
    else:
        return (-waypoint_y, waypoint_x)

def day12b(array):
    waypoint_x = 10
    waypoint_y = 1
    ship_x = 0
    ship_y = 0
    for line in array:
        direction = line[0]
        value = int(line[1:])
        if direction == 'F':
            ship_x += value * waypoint_x
            ship_y += value * waypoint_y
        if direction == 'R':
            waypoint_x, waypoint_y = rotate_waypoint(direction, value, waypoint_x, waypoint_y)
        elif direction == 'L':
            waypoint_x, waypoint_y = rotate_waypoint(direction, value, waypoint_x, waypoint_y)
        elif direction == 'N':
            waypoint_y += value
        elif direction == 'E':
            waypoint_x += value
        elif direction == 'S':
            waypoint_y -= value
        elif direction == 'W':
            waypoint_x -= value
    print("Part 2:", abs(ship_x) + abs(ship_y))

if __name__ == "__main__":
    filename = "input12.txt"
    arr = arrayise(filename)
    day12a(arr)
    day12b(arr)