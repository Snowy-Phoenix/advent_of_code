def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def solve(array):
    sum = 0
    sum2 = 0
    for line in array:
        game_games = line.split(":")
        gameid = int(game_games[0].split()[1])
        games = game_games[1].split(";")
        possible = True
        red = 0
        blue = 0
        green = 0
        for g in games:
            cubes = g.split(",")
            for c in cubes:
                n, color = c.split()
                n = int(n.strip())
                color = color.strip()
                if color == "red":
                    red = max(n, red)
                    if n > 12:
                        possible = False
                elif color == "green":
                    green = max(n, green)
                    if n > 13:
                        possible = False
                elif color == "blue":
                    blue = max(n, blue)
                    if n > 14:
                        possible = False
                else:
                    print("?")
        if possible:
            sum += gameid
        print(gameid, red, blue, green)
        sum2 += red*blue*green
    print(sum)
    print(sum2)


if __name__ == '__main__':
    filename = "input2.txt"
    arr = arrayise(filename)
    solve(arr)