
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

def make_move(board, player, row, col):
    if not is_valid_move(board, player, row, col):
        return False
    board[row][col] = player
    for differenceRow in [-1, 0, 1]:
        for differenceColumn in [-1, 0, 1]:
            if differenceRow == 0 and differenceColumn == 0:
                continue
            newRow, newColumn = row + differenceRow, col + differenceColumn
            to_flip = []
            while 0 <= newRow < N and 0 <= newColumn < N and board[newRow][newColumn] == -player:
                to_flip.append((newRow, newColumn))
                newRow += differenceRow
                newColumn += differenceColumn
            if 0 <= newRow < N and 0 <= newColumn < N and board[newRow][newColumn] == player:
                for flip_row, flip_col in to_flip:
                    board[flip_row][flip_col] = player
    return True

def get_score(board):
    black_score = sum(row.count(BLACK) for row in board)
    white_score = sum(row.count(WHITE) for row in board)
    return black_score, white_score

if __name__ == "__main__":
    print_board(initialize_board())
