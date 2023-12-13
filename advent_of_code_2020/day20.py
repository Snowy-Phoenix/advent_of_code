import re
import numpy as np

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

class ImageTile:
    def __init__(self, id, image):
        self.id = id
        self.image = np.array(image)
        self.borders = set()
        self.border_to_edge_data = dict() # border pattern, tuple (rotation, flipped)
        self.edge_to_border_data = dict() # tuple(rotation, flipped), border pattern
        self.compute_border()

        # Assumes that the initialisation is the right way.
        self.rotation = 0 # Side facing up: 0 - up, 1 - right, 2 - down, 3 - left
        self.flipped = False # Flipped horizontally, while rotation = 0

    def compute_border(self):

        # Top
        top = ""
        for i in range(len(self.image)):
            top += self.image[0][i]
        top_r = "".join(reversed(top))

        # Bottom
        bottom = ""
        for i in range(len(self.image) - 1, -1, -1):
            bottom += self.image[-1][i]
        bottom_r = "".join(reversed(bottom))

        # Left
        left = ""
        for i in range(len(self.image) - 1, -1, -1):
            left += self.image[i][0]
        left = left
        left_r = "".join(reversed(left))

        # Right
        right = ""
        for i in range(len(self.image)):
            right += self.image[i][-1]
        right = right
        right_r = "".join(reversed(right))
        
        self.borders.add(top)
        self.borders.add(bottom)
        self.borders.add(left)
        self.borders.add(right)
        self.borders.add(top_r)
        self.borders.add(bottom_r)
        self.borders.add(left_r)
        self.borders.add(right_r)

        self.border_to_edge_data[top] = (0, False)
        self.border_to_edge_data[top_r] = (0, True)
        self.border_to_edge_data[right] = (1, False)
        self.border_to_edge_data[left_r] = (1, True) # Flipped.
        self.border_to_edge_data[bottom] = (2, False)
        self.border_to_edge_data[bottom_r] = (2, True)
        self.border_to_edge_data[left] = (3, False)
        self.border_to_edge_data[right_r] = (3, True)

        for value in self.border_to_edge_data:
            key = self.border_to_edge_data[value]
            self.edge_to_border_data[key] = value

    def get_flipped_image(self):
        image = []
        for i in range(len(self.image)):
            row = self.image[i]
            image.append([])
            for j in range(len(row) - 1, -1, -1):
                image[i].append(row[j])
        return image

    def get_current_image(self, has_borders=True):
        new_image = self.image
        if not has_borders:
            new_image = new_image[1:-1, 1:-1]
        if self.flipped:
            new_image = np.fliplr(new_image)
        new_image = np.rot90(new_image, self.rotation)
        return new_image

    def get_str_image(self, show_borders=True):
        row_start = {0:0, 1:0, 2:len(self.image)-1, 3:len(self.image)-1}
        row_end = {0:len(self.image), 1:len(self.image), 2:-1, 3:-1}
        row_dir = {0:1, 1:1, 2:-1, 3:-1}
        col_start = {0:0, 1:len(self.image)-1, 2:len(self.image)-1, 3:0}
        col_end = {0:len(self.image), 1:-1, 2:-1, 3:len(self.image)}
        col_dir = {0:1, 1:-1, 2:-1, 3:1}
        rot = self.rotation

        image = self.image
        if self.flipped:
            image = self.get_flipped_image()

        br = 0
        bc = 0
        if not show_borders:
            br = 1
            bc = 1
        br *= row_dir[rot]
        bc *= col_dir[rot]

        string = ""
        if rot % 2 == 0:
            for i in range(row_start[rot] + br, row_end[rot] - br, row_dir[rot]):
                for j in range(col_start[rot] + bc, col_end[rot] - bc, col_dir[rot]):
                    c = image[i][j]
                    string += c
                string += "\n"
        else:
            for i in range(col_start[rot] + bc, col_end[rot] - bc, col_dir[rot]):
                for j in range(row_start[rot] + br, row_end[rot] - br, row_dir[rot]):
                    c = image[j][i]
                    string += c
                string += "\n"
        return string
    
    def set_orientation(self, rotation, flipped):
        self.rotation = rotation
        self.flipped = flipped

    def get_border(self, side):
        """
        Gets the relative up, right, down, left.
        0 = up, 1 = right, 2 = down, 3 = left
        """
        return self.edge_to_border_data[((side + self.rotation) % 4, self.flipped)]

    def orient_image_to_border(self, border, border_orientation):
        reversed_border = "".join(reversed(border))
        orientation = self.border_to_edge_data[reversed_border]
        a = 0
        if border_orientation % 2 == 0:
            a = 2
        self.set_orientation((orientation[0] + border_orientation + a) % 4, orientation[1])

    def __str__(self):
       return "Tile id: " + str(self.id) + "\n" + self.get_str_image()
    
    def __repr__(self):
        return str(self.id)

class FullImage:
    def __init__(self, images):
        self.images = images
        self.image_border_data = self.compute_border_data()
        self.image_edges_data = None
        self.image_edges = None
        self.image_corners = None
        self.get_image_edges_and_corners()
        self.full_image = None
        self.full_image_array = None

    def compute_border_data(self):
        border_counts = dict() # border pattern, [images with this border]
        for i in self.images:
            for b in i.borders:
                if b in border_counts:
                    border_counts[b].append(i)
                else:
                    border_counts[b] = [i]
        return border_counts

    def get_image_edges_data(self):
        edge_image_tile_counts = dict()
        for i in self.image_border_data:
            if len(self.image_border_data[i]) == 1:
                tile = self.image_border_data[i][0]
                if tile in edge_image_tile_counts:
                    edge_image_tile_counts[tile] += 1
                else:
                    edge_image_tile_counts[tile] = 1
        return edge_image_tile_counts

    def get_image_edges(self):
        edges = []
        for i in self.image_edges_data:
            if self.image_edges_data[i] == 2:
                edges.append(i)
        return edges

    def get_image_corners(self):
        corners = []
        for i in self.image_edges_data:
            if self.image_edges_data[i] == 4:
                corners.append(i)
        return corners

    def get_image_edges_and_corners(self):
        self.image_edges_data = self.get_image_edges_data()
        self.image_edges = self.get_image_edges()
        self.image_corners = self.get_image_corners()

    def get_other_image_bordering(self, image_id, border):
        b = self.image_border_data[border]
        if len(b) == 1:
            return None
        if b[0].id == image_id:
            return b[1]
        return b[0]

    def assemble_image(self):

        assembled_image = []

        starting_corner = self.image_corners[3] # Top left corner

        # Get the correct orientation. Assume that the corner is not flipped.
        starting_rotation = 3
        for i in range(1, 4):
            border1 = starting_corner.edge_to_border_data[(i - 1, False)]
            border2 = starting_corner.edge_to_border_data[(i, False)]
            if len(self.image_border_data[border1]) == 1:
                if len(self.image_border_data[border2]) == 2:
                    starting_rotation = i - 1
                    break
        starting_corner.set_orientation(starting_rotation, False)
        assembled_image.append([starting_corner])

        prev_image = starting_corner
        leftmost_image = prev_image
        while True:
            while True:
                r_border = prev_image.get_border(1)
                curr_image = self.get_other_image_bordering(prev_image.id, r_border)
                if curr_image == None:
                    break
                else:
                    curr_image.orient_image_to_border(r_border, 1)
                    prev_image = curr_image
                    assembled_image[-1].append(curr_image)
                    
            b_border = leftmost_image.get_border(2)
            bottom_image = self.get_other_image_bordering(leftmost_image.id, b_border)
            if bottom_image == None:
                break
            else:
                bottom_image.orient_image_to_border(b_border, 2)
                prev_image = bottom_image
                leftmost_image = bottom_image
                assembled_image.append([bottom_image])
        self.full_image = assembled_image
        self.create_image_as_array()

    def create_image_as_array(self):
        rows = len(self.full_image)
        cols = len(self.full_image[0])
        full_image = []
        for r in range(len(self.full_image)):
            row = self.full_image[r]
            full_image.append([])
            for image in row:
                full_image[r].append(image.get_current_image(has_borders=False))
        image_rows = len(full_image[0][0])
        image_cols = len(full_image[0][0][0])
        

        full_image = np.array(full_image)
        full_image = full_image.transpose(0, 2, 1, 3).reshape(rows * image_rows, cols * image_cols)

        self.full_image_array = full_image

def is_monster_here(image, monster, row, col):
    for r in range(len(monster)):
        for c in range(len(monster[0])):
            monster_tile = monster[r][c]
            if monster_tile == 0:
                continue
            else:
                image_tile = image[row + r][col + c]
                if image_tile == '.':
                    return False
    return True

def mark_monsters(image, locations, monster, rotation, flipped):
    marked_image = np.copy(image)
    m = monster
    if flipped:
        m = np.fliplr(monster)
    m = np.rot90(m, rotation)

    for row, col in locations:
        for mr in range(len(m)):
            for mc in range(len(m[mr])):
                monster_tile = m[mr][mc]
                image_tile = image[row + mr][col + mc]
                if monster_tile:
                    if image_tile == '.':
                        print("Error: invalid monster at r:{} c:{}".format(row, col))
                    else:
                        marked_image[row + mr][col + mc] = 'O'
    marked_image = np.rot90(marked_image, 4 - rotation)
    if flipped:
        marked_image = np.fliplr(marked_image)
    return marked_image

def find_monster(image_array):
    monster = np.array([
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,1,1,1],
        [0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0]
    ])
    current_monster = monster
    monster_rotation = 0
    monster_flipped = False
    monster_found = False
    monster_locations = []
    monster_orientations = 0
    for flipped in range(2):
        for rotation in range(4):
            if flipped:
                current_monster = np.fliplr(monster)
            else:
                current_monster = monster
            current_monster = np.rot90(current_monster, rotation)
            for row in range(len(image_array) - len(current_monster)):
                for col in range(len(image_array[0]) - len(current_monster[0])):
                    result = is_monster_here(image_array, current_monster, row, col)
                    if result:
                        monster_found = True
                        monster_locations.append((row, col))
            if monster_found:
                monster_rotation = rotation
                monster_flipped = bool(flipped)
                monster_orientations += 1
                monster_found = False
    marked_map = mark_monsters(image_array, monster_locations, monster, monster_rotation, monster_flipped)
    m = np.rot90(image_array, 4 - monster_rotation)
    if monster_flipped:
        m = np.fliplr(m)
    np.savetxt('unmarked_map.txt', m, fmt='%c', delimiter='')
    np.savetxt('marked_map.txt', marked_map, fmt='%c', delimiter='')
    print("Part 2:", (marked_map == '#').sum())
    

def day20(array):
    is_processing_image = False
    processed_image = []
    id = None
    images = []
    for line in array:
        if line == "":
            is_processing_image = False
            images.append(ImageTile(id, processed_image))
            processed_image.clear()
            continue
        else:
            if is_processing_image:
                processed_image.append([x for x in line])
            else:
                id = re.fullmatch("Tile (\d+):", line).group(1)
                is_processing_image = True
    images.append(ImageTile(id, processed_image))

    full_image = FullImage(images)

    value = 1
    for i in full_image.image_corners:
        value *= int(i.id)
    print("Part 1:", value)
    full_image.assemble_image()
    find_monster(full_image.full_image_array)

if __name__ == "__main__":
    filename = "input20.txt"
    arr = arrayise(filename)
    day20(arr)