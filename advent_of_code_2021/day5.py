class LineIntersectMap:

    def __init__(self):
        self.grid = [[0 for j in range(1000)] for i in range(1000)]
        self.intersections = 0

    def add_line(self, x1, y1, x2, y2, include_diagonals=False):

        # Horizontal line
        if (y1 == y2):
            if x1 < x2:
                for i in range(x2 - x1 + 1):
                    self.grid[y1][x1 + i] += 1
                    tile = self.grid[y1][x1 + i]
                    if tile == 2:
                        self.intersections += 1
            else:
                for i in range(x1 - x2 + 1):
                    self.grid[y1][x2 + i] += 1
                    tile = self.grid[y1][x2 + i]
                    if tile == 2:
                        self.intersections += 1

        # Vertical line
        elif (x1 == x2):
            if y1 < y2:
                for i in range(y2 - y1 + 1):
                    self.grid[y1 + i][x1] += 1
                    tile = self.grid[y1 + i][x1]
                    if tile == 2:
                        self.intersections += 1
            else:
                for i in range(y1 - y2 + 1):
                    self.grid[y2 + i][x1] += 1
                    tile = self.grid[y2 + i][x1]
                    if tile == 2:
                        self.intersections += 1

        # Diagonal
        elif include_diagonals:
            sign_x = int(x1 < x2) * 2 - 1
            sign_y = int(y1 < y2) * 2 - 1
            curr_x = x1
            curr_y = y1
            while (curr_x != x2):
                self.grid[curr_y][curr_x] += 1
                tile = self.grid[curr_y][curr_x]
                if tile == 2:
                    self.intersections += 1
                curr_x += sign_x
                curr_y += sign_y
            # Do this for the endpoint
            self.grid[curr_y][curr_x] += 1
            tile = self.grid[curr_y][curr_x]
            if tile == 2:
                self.intersections += 1
            curr_x += sign_x
            curr_y += sign_y

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day5(array, include_diagonals=False):
    intersect_map = LineIntersectMap()
    for line in array:
        coords = line.split(" -> ")
        x1, y1 = coords[0].split(",")
        x2, y2 = coords[1].split(",")
        x1 = int(x1)
        x2 = int(x2)
        y1 = int(y1)
        y2 = int(y2)
        intersect_map.add_line(x1, y1, x2, y2, include_diagonals)
    return intersect_map.intersections

if __name__ == "__main__":
    filename = "input5.txt"
    arr = arrayise(filename)
    print(day5(arr))
    print(day5(arr, include_diagonals = True))
