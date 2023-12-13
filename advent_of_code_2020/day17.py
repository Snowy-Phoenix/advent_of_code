import re

class ConwayTile:
    def __init__(self, is_alive):
        self.is_alive = is_alive
        self.neighbours = 0
        self.is_ticking = False

    def __repr__(self):
        if self.is_alive:
            return "#"
        return "."

    def add_neighbour(self):
        self.neighbours += 1
    
    def tick(self):
        if self.is_alive:
            if self.neighbours < 3 or self.neighbours > 4:
               self.is_alive = False
        else:
            if self.neighbours == 3:
                self.is_alive = True
        self.neighbours = 0
        self.is_ticking = False
        return self.is_alive
             
    
class ConwayCubeBoard:
    def __init__(self, board):
        self.num_alive = 0
        self.tiles_to_tick = []
        self.schedule_pad_board = False
        self.board = self.parse_board(board)

    def parse_board(self, board):
        r = 0
        parsed_board = []
        for row in board:
            parsed_board.append([])
            for tile in row:
                if tile == '.':
                    parsed_board[r].append(ConwayTile(False))
                else:
                    parsed_board[r].append(ConwayTile(True))
                    self.num_alive += 1
            r += 1
        
        conway_cube_board = [parsed_board]
        conway_cube_board = self.pad_board(conway_cube_board)
        return conway_cube_board

    def generate_empty_row(self, length):
        row = []
        for i in range(length):
            row.append(ConwayTile(False))
        return row

    def generate_empty_plane(self, rows, cols):
        plane = []
        for r in range(rows):
            plane.append(self.generate_empty_row(cols))
        return plane

    def pad_board(self, board=None):
        if board == None:
            board = self.board
        
        # Firstly, expand the edges of each board plane
        for plane in board:
            # Extend each row
            for row in plane:
                row.insert(0, ConwayTile(False))
                row.append(ConwayTile(False))
            # Add top and bottom row
            col_length = len(plane[0])
            plane.insert(0, self.generate_empty_row(col_length))
            plane.append(self.generate_empty_row(col_length))
        
        # Create the two empty planes for the top and bottom
        row_length = len(board[0])
        col_length = len(board[0][0])
        board.insert(0, self.generate_empty_plane(row_length, col_length))
        board.append(self.generate_empty_plane(row_length, col_length))
        return board

    def is_at_boundary(self, z, r, c):
        if z == 0 or z == len(self.board) - 1:
            return True
        elif r == 0 or r == len(self.board[0]) - 1:
            return True
        elif c == 0 or c == len(self.board[0][0]) - 1:
            return True
        return False

    def tick_neighbours(self, z, r, c):
        values = [-1, 0, 1]
        for z_offset in values:
            for r_offset in values:
                for c_offset in values:
                    tile = self.board[z + z_offset][r + r_offset][c + c_offset]
                    tile.add_neighbour()
                    if (not tile.is_ticking):
                        tile.is_ticking = True
                        self.tiles_to_tick.append(tile)
                    if not self.schedule_pad_board:
                        if self.is_at_boundary(z + z_offset, r + r_offset, c + c_offset):
                            self.schedule_pad_board = True
                    

    def tick_tiles(self):
        for tile in self.tiles_to_tick:
            is_alive = tile.is_alive
            is_alive_after_tick = tile.tick()
            if (is_alive and not is_alive_after_tick):
                self.num_alive -= 1
            elif (not is_alive and is_alive_after_tick):
                self.num_alive += 1
        self.tiles_to_tick.clear()

    def simulate(self):
        for z in range(len(self.board)):
            plane = self.board[z]
            for r in range(len(plane)):
                row = plane[r]
                for c in range(len(row)):
                    tile = row[c]
                    if tile.is_alive:
                        self.tick_neighbours(z, r, c)
        self.tick_tiles()
        if self.schedule_pad_board:
            self.pad_board() 
            self.schedule_pad_board = False

    def __str__(self):
        output = ""
        for plane_n in range(len(self.board)):
            output += "z={}\n".format(plane_n)
            plane = self.board[plane_n]
            for row in plane:
                for tile in row:
                    output += str(tile)
                output += "\n"
            output += "\n"
        output += "Number alive: {}".format(self.num_alive)
        return output

class ConwayHypercubeBoard:
    def __init__(self, board):
        self.num_alive = 0
        self.tiles_to_tick = []
        self.schedule_pad_board = False
        self.board = self.parse_board(board)

    def parse_board(self, board):
        r = 0
        parsed_board = []
        for row in board:
            parsed_board.append([])
            for tile in row:
                if tile == '.':
                    parsed_board[r].append(ConwayTile(False))
                else:
                    parsed_board[r].append(ConwayTile(True))
                    self.num_alive += 1
            r += 1
        
        conway_board = [[parsed_board]]
        conway_board = self.pad_board(conway_board)
        return conway_board

    def generate_empty_row(self, length):
        row = []
        for i in range(length):
            row.append(ConwayTile(False))
        return row

    def generate_empty_plane(self, rows, cols):
        plane = []
        for r in range(rows):
            plane.append(self.generate_empty_row(cols))
        return plane

    def generate_empty_space(self, height, rows, cols):
        space = []
        for i in range(height):
            space.append(self.generate_empty_plane(rows, cols))
        return space

    def pad_board(self, board=None):
        if board == None:
            board = self.board
        
        # Firstly, expand the edges of each board plane
        for space in board:
            for plane in space:
                # Extend each row
                for row in plane:
                    row.insert(0, ConwayTile(False))
                    row.append(ConwayTile(False))
                # Add top and bottom row
                col_length = len(plane[0])
                plane.insert(0, self.generate_empty_row(col_length))
                plane.append(self.generate_empty_row(col_length))
        # Create the two empty planes for the top and bottom
        for space in board:
            row_length = len(space[0])
            col_length = len(space[0][0])
            space.insert(0, self.generate_empty_plane(row_length, col_length))
            space.append(self.generate_empty_plane(row_length, col_length))

        # Create two empty 3d spaces for +-w.
        height = len(board[0])
        row_length = len(board[0][0])
        col_length = len(board[0][0][0])
        board.insert(0, self.generate_empty_space(height, row_length, col_length))
        board.append(self.generate_empty_space(height, row_length, col_length))
        return board

    def is_at_boundary(self, z, r, c, w):
        if w == 0 or w == len(self.board) - 1:
            return True
        elif z == 0 or z == len(self.board[0]) - 1:
            return True
        elif r == 0 or r == len(self.board[0][0]) - 1:
            return True
        elif c == 0 or c == len(self.board[0][0][0]) - 1:
            return True
        return False

    def tick_neighbours(self, z, r, c, w):
        values = [-1, 0, 1]
        for w_offset in values:
            for z_offset in values:
                for r_offset in values:
                    for c_offset in values:
                        tile = self.board[w + w_offset][z + z_offset][r + r_offset][c + c_offset]
                        tile.add_neighbour()
                        if (not tile.is_ticking):
                            tile.is_ticking = True
                            self.tiles_to_tick.append(tile)
                        if not self.schedule_pad_board:
                            if self.is_at_boundary(z + z_offset, r + r_offset, c + c_offset, w + w_offset):
                                self.schedule_pad_board = True
                    

    def tick_tiles(self):
        for tile in self.tiles_to_tick:
            is_alive = tile.is_alive
            is_alive_after_tick = tile.tick()
            if (is_alive and not is_alive_after_tick):
                self.num_alive -= 1
            elif (not is_alive and is_alive_after_tick):
                self.num_alive += 1
        self.tiles_to_tick.clear()

    def simulate(self):
        for w in range(len(self.board)):
            space = self.board[w]
            for z in range(len(space)):
                plane = space[z]
                for r in range(len(plane)):
                    row = plane[r]
                    for c in range(len(row)):
                        tile = row[c]
                        if tile.is_alive:
                            self.tick_neighbours(z, r, c, w)
        self.tick_tiles()
        if self.schedule_pad_board:
            self.pad_board() 
            self.schedule_pad_board = False

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day17(array, cycles=6):
    cubic_board = ConwayCubeBoard(array)
    for i in range(cycles):
        cubic_board.simulate()
    # print(cubic_board)
    print("Part 1:", cubic_board.num_alive)
    hypercubic_board = ConwayHypercubeBoard(array)
    for i in range(cycles):
        hypercubic_board.simulate()
    print("Part 2:", hypercubic_board.num_alive)

if __name__ == "__main__":
    filename = "input17.txt"
    arr = arrayise(filename)
    day17(arr)