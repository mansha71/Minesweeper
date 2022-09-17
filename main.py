import random
import re

# creating board object, creates new board


class gameBoard:
    def __init__(self, size, bombs):

        self.size = size
        self.bombs = bombs

        # making the board
        self.board = self.make_new_board()

        self.assign_values()

        # set to keep track of what has been dug
        self.dug = set()

    def make_new_board(self):

        # makiing empty board
        board = [[None for _ in range(self.size)] for _ in range(self.size)]

        # planting bombs:
        current_bombs = 0
        while current_bombs < self.bombs:
            row = random.randint(0, self.size-1)
            col = random.randint(0, self.size-1)
            if board[row][col] == '*':
                continue
            else:
                board[row][col] = '*'
                current_bombs += 1
        return board

    def assign_values(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        num_bombs = 0
        for r in range(max(0, row - 1), min(self.size-1, (row + 1)) + 1):
            for c in range(max(0, col - 1), min(self.size-1, col + 1) + 1):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    num_bombs = +1
        return num_bombs

    def dig(self, row, col):

        self.dug.add((row, col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row - 1), min(self.size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.size - 1, col + 1) + 1):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)

        return True

    def __str__(self):
        visible_board = [[None for _ in range(
            self.size)] for _ in range(self.size)]

        for row in range(self.size):
            for col in range(self.size):
                if (row, col) in self . dug:
                    visible_board[row][col] = str(self.board[row][col])

                else:
                    visible_board[row][col] = ' '
            # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


def play(size=10, bombs=10):
    board = gameBoard(size, bombs)

    while len(board.dug) < board.size**2-bombs:
        print(board)
        user_input = re.split(
            ',(\\s)*', input("Where do you want to dig? Input as row,col: "))
        row, col = int(user_input[0]), int(user_input[-1])

        if row < 0 or row >= board.size or col < 0 or col >= size:
            print("Enter a Real Location. Try Again:")
            continue

        safe = board.dig(row, col)
        if not safe:
            break
    if safe:
        print('YOU WON!!')
    else:
        print('GAME OVER')
        board.dug = [(r, c) for r in range(board.size)
                     for c in range(board.size)]


if __name__ == '__main__':
    play()
