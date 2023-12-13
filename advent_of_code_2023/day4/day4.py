def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def solve(array):
    sum = 0
    cardsWon = 0
    cards = [1 for _ in array]
    for line in array:
        winners, number = line.split("|")
        cardi, winners = winners.split(":")
        cardi = int(cardi.split()[1])

        winners = list(map(int, winners.split()))
        number = list(map(int, number.split()))
        ncards = cards[cardi - 1]
        i = 0
        j = 1
        for n in number:
            if n in winners:
                cards[cardi - 1 + j] += ncards
                if i == 0:
                    i = 1
                else:
                    i *= 2
                j += 1
        sum += i
        cardsWon += ncards

    print(sum)
    print(cardsWon)
    pass


if __name__ == '__main__':
    filename = "input4.txt"
    arr = arrayise(filename)
    solve(arr)