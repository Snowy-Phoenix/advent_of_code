class Position:
    def __init__(self, use_aim=False):
        self.x = 0
        self.depth = 0
        self.aim = 0
        self.use_aim = use_aim

    def move(self, direction, units):
        if self.use_aim:
            self.move_aim(direction, units)
            return
        if (direction == "forward"):
            self.x += units
        elif (direction == "down"):
            self.depth += units
        elif (direction == "up"):
            self.depth -= units

    def move_aim(self, direction, units):
        if (direction == "forward"):
            self.x += units
            self.depth += units * self.aim
        if (direction == "down"):
            self.aim += units
        if (direction == "up"):
            self.aim -= units

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line)
    return array

def day2(array, use_aim=False):
    p = Position(use_aim)
    for line in arr:
        direction, raw_units = line.split(' ')
        units = int(raw_units.strip())
        p.move(direction, units)
    return p.x * p.depth

if __name__ == "__main__":
    filename = "input2.txt"
    arr = arrayise(filename)
    print(day2(arr))
    print(day2(arr, use_aim=True))