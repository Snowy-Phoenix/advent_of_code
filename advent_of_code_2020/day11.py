import re

class Seat:

    def __init__(self, is_seat, part2=False):
        self.is_seat = is_seat
        self.is_occupied = False
        self.nearby_occupied_seats = 0
        self.part2 = part2

    def __repr__(self):
        if self.is_seat:
            if self.is_occupied:
                return "#"
            else:
                return "L"
        return "."

    def increment_occupied_seats(self):
        self.nearby_occupied_seats += 1
    
    def clear(self):
        self.nearby_occupied_seats = 0

    def tick(self):
        threshold = 4
        if (self.part2):
            threshold = 5
        changed = False
        if self.is_seat:
            if self.is_occupied:
                if self.nearby_occupied_seats >= threshold:
                    self.is_occupied = False
                    changed = True
            else:
                if self.nearby_occupied_seats == 0:
                    self.is_occupied = True
                    changed = True
        self.clear()
        return changed


class SeatLayout:

    def __init__(self, part2=False):
        self.seats = []
        self.part2 = part2
    
    def import_board(self, board_array):
        for row in board_array:
            self.seats.append([])
            for tile_i in range(len(row)):
                tile = row[tile_i]
                if tile == "L":
                    self.seats[-1].append(Seat(True, self.part2))
                else:
                    self.seats[-1].append(Seat(False, self.part2))

    def get_num_occupied(self):
        n = 0
        for row in self.seats:
            for seat in row:
                n += seat.is_occupied
        return n

    def __repr__(self):
        string = ""
        for row in self.seats:
            string += str(row)
            string += ",\n"
        return string

    def increment_occupied1(self, row_n, col_n):
        for i in range(3):
            if (row_n - 1 + i < 0 or row_n - 1 + i >= len(self.seats)):
                continue
            for j in range(3):
                if (col_n - 1 + j < 0 or col_n - 1 + j >= len(self.seats[row_n])):
                    continue
                elif (i == 1 and j == 1):
                    continue
                else:
                    self.seats[row_n - 1 + i][col_n - 1 + j].increment_occupied_seats()

    def add_vector(self, row_n, col_n, vector):
        return (row_n + vector[0], col_n + vector[1])

    def increment_occupied2(self, row_n, col_n):
        directions = [(-1,-1), (-1,1), (1,-1), (1,1), (1,0), (-1,0), (0,1), (0,-1)]
        for direction in directions:
            r, c = self.add_vector(row_n, col_n, direction)
            while (0 <= r < len(self.seats)) and (0 <= c < len(self.seats[row_n])):
                seat = self.seats[r][c]
                if seat.is_seat:
                    seat.increment_occupied_seats()
                    break
                r, c = self.add_vector(r, c, direction)


    def simulate(self, part2=False):
        for row_n in range(len(self.seats)):
            for col_n in range(len(self.seats[row_n])):
                seat = self.seats[row_n][col_n]
                if seat.is_occupied:
                    if part2:
                        self.increment_occupied2(row_n, col_n)
                    else:
                        self.increment_occupied1(row_n, col_n)
                    
        changed = 0
        for row in self.seats:
            for seat in row:
                changed += seat.tick()
        return bool(changed)

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day11a(array):
    layout = SeatLayout()
    layout.import_board(array)
    changed = True
    while changed:
        changed = layout.simulate()
    print("Part 1:", layout.get_num_occupied())

def day11b(array):
    layout = SeatLayout(part2=True)
    layout.import_board(array)
    changed = True
    while changed:
        changed = layout.simulate(part2=True)
    print("Part 2:", layout.get_num_occupied())

if __name__ == "__main__":
    filename = "input11.txt"
    arr = arrayise(filename)
    day11a(arr)
    day11b(arr)