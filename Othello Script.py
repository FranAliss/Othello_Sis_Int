
def initialize_board():
    board = [[0] * 8 for _ in range(8)]
    board[3][3] = 1
    board[3][4] = -1
    board[4][3] = -1
    board[4][4] = 1
    return board

def print_board(board):
    print("  0 1 2 3 4 5 6 7")
    for i in range(8):
        row = str(i) + " "
        for j in range(8):
            if board[i][j] == 0:
                row += ". "
            elif board[i][j] == 1:
                row += "X "
            else:
                row += "O "
        print(row)

if __name__ == "__main__":
    print_board(initialize_board())
