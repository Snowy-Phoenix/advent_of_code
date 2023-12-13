class BingoBoard:

    def __init__(self):
        self.board = [[False for j in range(5)] for i in range(5)]
        self.numbers = dict() #Key: number. Value: Tuple of (row, col)
        self.unfilled_row = 0
        self.unfilled_col = 0

    def play(self, number):
        if self.numbers.get(number) == None:
            return False

        row, col = self.numbers[number]
        self.board[row][col] = True
        
        # Check row
        for i in range(5):
            if self.board[row][i] == False:
                break
            else:
                if i == 4:
                    return True
        
        # Check col
        for i in range(5):
            if self.board[i][col] == False:
                break
            else:
                if i == 4:
                    return True
        return False

    def compute_score(self, number):
        score = 0
        for n in self.numbers.keys():
            row, col = self.numbers[n]
            if self.board[row][col] == False:
                score += n
        return score * number

    def fill_board(self, number):
        if self.unfilled_row > 5:
            raise Exception
        self.numbers[number] = (self.unfilled_row, self.unfilled_col)
        self.unfilled_col = (self.unfilled_col + 1) % 5
        if (self.unfilled_col == 0):
            self.unfilled_row += 1


def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day4(array, win=True):

    drawn_numbers = array[0].split(',')
    for i in range(len(drawn_numbers)):
        drawn_numbers[i] = int(drawn_numbers[i])

    bingo_boards = []

    for line in array[1:]:
        line = line.strip()
        if line == "":
            bingo_boards.append(BingoBoard())
        else:
            numbers = line.split(' ')
            for n in numbers:
                if n != '':
                    bingo_boards[-1].fill_board(int(n))
    
    for number in drawn_numbers:
        i = 0
        while (i < len(bingo_boards)):
            board = bingo_boards[i]
            if board.play(number):
                if (win):
                    return board.compute_score(number)
                else:
                    if (len(bingo_boards) == 1):
                        return board.compute_score(number)
                    else:
                        bingo_boards.remove(board)
            else:
                i += 1

if __name__ == "__main__":
    filename = "input4.txt"
    arr = arrayise(filename)
    print(day4(arr, win=True))
    print(day4(arr, win=False))