
N = 8

EMPTY = 0
BLACK = 1
WHITE = -1

def initialize_board():
    board = [[EMPTY] * N for _ in range(N)]
    board[3][3] = BLACK
    board[3][4] = WHITE
    board[4][3] = WHITE
    board[4][4] = BLACK
    return board

def print_board(board):
    print("  0 1 2 3 4 5 6 7")
    for i in range(N):
        row = str(i) + " "
        for j in range(N):
            if board[i][j] == EMPTY:
                row += ". "
            elif board[i][j] == BLACK:
                row += "X "
            else:
                row += "O "
        print(row)

def is_valid_move(board, player, row, col):
    if board[row][col] != EMPTY:
        return False
    for differencRow in [-1, 0, 1]:
        for differencColumn in [-1, 0, 1]:
            if differencRow == 0 and differencColumn == 0:
                continue
            newRow, newColumn = row + differencRow, col + differencColumn
            while 0 <= newRow < N and 0 <= newColumn < N and board[newRow][newColumn] == -player:
                newRow += differencRow
                newColumn += differencColumn
            if 0 <= newRow < N and 0 <= newColumn < N and board[newRow][newColumn] == player:
                return True
    return False


if __name__ == "__main__":
    print_board(initialize_board())
