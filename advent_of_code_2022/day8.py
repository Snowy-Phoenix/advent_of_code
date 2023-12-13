def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array


def get_visible_up(trees):
    visible = set()
    for col, tree in enumerate(trees[0]):
        tree_h = tree
        visible.add((0, col))
        i = 1
        while True:
            if i >= len(trees):
                break
            new_tree = trees[i][col]
            if new_tree > tree_h:
                tree_h = new_tree
                visible.add((i, col))
            elif new_tree == 9:
                break
            i += 1
    return visible


def get_visible_down(trees):
    visible = set()
    for col, tree in enumerate(trees[-1]):
        tree_h = tree
        visible.add((len(trees[col]) - 1, col))
        i = 1
        while True:
            if i >= len(trees):
                break
            new_tree = trees[len(trees[col]) - i - 1][col]
            if new_tree > tree_h:
                tree_h = new_tree
                visible.add((len(trees[col]) - i - 1, col))
            elif new_tree == 9:
                break
            elif i >= len(trees):
                break
            i += 1
    return visible


def get_visible_left(trees):
    visible = set()
    for row in range(len(trees)):
        tree_h = trees[row][0]
        visible.add((row, 0))
        i = 1
        while True:
            if i >= len(trees):
                break
            new_tree = trees[row][i]
            if new_tree > tree_h:
                tree_h = new_tree
                visible.add((row, i))
            elif new_tree == 9:
                break
            elif i >= len(trees):
                break
            i += 1
    return visible


def get_visible_right(trees):
    visible = set()
    for row in range(len(trees)):
        tree_h = trees[row][-1]
        visible.add((row, len(trees) - 1))
        i = 1
        while True:
            if i >= len(trees):
                break
            new_tree = trees[row][len(trees[row]) - i - 1]
            if new_tree > tree_h:
                tree_h = new_tree
                visible.add((row, (len(trees[row]) - i - 1)))
            elif new_tree == 9:
                break
            elif i >= len(trees):
                break
            i += 1
    return visible


def solve_part1(trees):
    visible = set()  # (row, col)
    visible = visible.union(get_visible_up(trees))
    visible = visible.union(get_visible_down(trees))
    visible = visible.union(get_visible_left(trees))
    visible = visible.union(get_visible_right(trees))

    print("Part 1:", len(visible))


def get_viewing_distance_up(trees, r, c):
    tree_h = trees[r][c]
    visible = 0
    i = 1
    while r - i >= 0:
        t = trees[r - i][c]
        if (t < tree_h):
            visible += 1
        else:
            visible += 1
            return visible
        i += 1
    return visible


def get_viewing_distance_down(trees, r, c):
    tree_h = trees[r][c]
    visible = 0
    i = 1
    while r + i < len(trees):
        t = trees[r + i][c]
        if (t < tree_h):
            visible += 1
        else:
            visible += 1
            return visible
        i += 1
    return visible


def get_viewing_distance_right(trees, r, c):
    tree_h = trees[r][c]
    visible = 0
    i = 1
    while c + i < len(trees[r]):
        t = trees[r][c + i]
        if (t < tree_h):
            visible += 1
        else:
            visible += 1
            return visible
        i += 1
    return visible


def get_viewing_distance_left(trees, r, c):
    tree_h = trees[r][c]
    visible = 0
    i = 1
    while c - i >= 0:
        t = trees[r][c - i]
        if (t < tree_h):
            visible += 1
        else:
            visible += 1
            return visible
        i += 1
    return visible


def solve_part2(trees):
    max_scenic_score = 0
    for r, row in enumerate(trees):
        for c in range(len(row)):
            up = get_viewing_distance_up(trees, r, c)
            right = get_viewing_distance_right(trees, r, c)
            left = get_viewing_distance_left(trees, r, c)
            down = get_viewing_distance_down(trees, r, c)
            scenic_score = up * right * left * down
            max_scenic_score = max(max_scenic_score, scenic_score)

    print("Part 2:", max_scenic_score)


def solve(array):
    trees = []
    for row in array:
        trees.append([])
        for tree in row:
            trees[-1].append(int(tree))
    solve_part1(trees)
    solve_part2(trees)


if __name__ == '__main__':
    filename = "input8.txt"
    arr = arrayise(filename)
    solve(arr)
