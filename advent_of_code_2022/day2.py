def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def get_outcome(opp_move, your_move):
    if opp_move == your_move:
        return 3
    elif (your_move == ((opp_move + 1) % 3)):
        return 6
    return 0

def part1(array):
    key = {'A':0, 'B':1, 'C':2, 'X':0, 'Y':1, 'Z':2}
    score = 0
    for lines in array:
        move = lines.split()
        opp_move = key[move[0]]
        your_move = key[move[1]]
        outcome = get_outcome(opp_move, your_move)
        score += ((your_move + 1)) + outcome
    print("Part 1:", score)

def part2(array):
    key = {'A':0, 'B':1, 'C':2, 'X':-1, 'Y':0, 'Z':1}
    score = 0
    for lines in array:
        move = lines.split()
        opp_move = key[move[0]]
        your_move = (opp_move + key[move[1]]) % 3
        outcome = get_outcome(opp_move, your_move)
        score += ((your_move + 1)) + outcome
    print("Part 2:", score)

def solve(array):
    part1(array)
    part2(array)


if __name__ == '__main__':
    filename = "input2.txt"
    arr = arrayise(filename)
    solve(arr)