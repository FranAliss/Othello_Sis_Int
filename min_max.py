import copy

N = 4
COUNTER = 0
EMPTY = 0
BLACK = 1
WHITE = -1

def initialize_board():
    board = [[EMPTY] * N for _ in range(N)]
    board[1][1] = BLACK
    board[1][2] = WHITE
    board[2][1] = WHITE
    board[2][2] = BLACK
    return board

def print_board(board):
    print("  0 1 2 3")
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

def is_valid_move(valid_moves, move):
    if move in valid_moves:
        return True
    return False

def get_player_tokens(board, player):
    player_tokens = []
    for row in range(N):
        for column in range(N):
            if board[row][column] == player:
                player_tokens.append((row, column))
    return player_tokens

def get_valid_moves(board, player):
    valid_moves = []
    for token in get_player_tokens(board, player):
        for differenceRow in [-1, 0, 1]: 
            for differenceColumn in [-1, 0, 1]:
                if differenceRow == 0 and differenceColumn == 0:
                    continue
                adyRow = token[0] + differenceRow
                adyCol = token[1] + differenceColumn
                
                if 0 <= adyRow < N and 0 <= adyCol < N and board[adyRow][adyCol] == -player:
                    while 0 <= adyRow < N and 0 <= adyCol < N and board[adyRow][adyCol] == -player:
                        adyRow += differenceRow
                        adyCol += differenceColumn
                        
                    if 0 <= adyRow < N and 0 <= adyCol < N and board[adyRow][adyCol] == EMPTY:
                        valid_moves.append((adyRow, adyCol))
    return valid_moves

def make_move(board, player, move):
    row = move[0]
    col = move[1]
    if not is_valid_move(get_valid_moves(board,player), move):
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

def terminal_test(board):
    return all(all(cell != EMPTY for cell in row) for row in board)


def Min_Max(board, player, maximizing_player):
    global COUNTER
    COUNTER += 1
    if terminal_test(board):
        return get_score(board)[1]
    
    valid_moves = get_valid_moves(board, player)
    if maximizing_player:
        best_move = None
        for move in valid_moves:
            new_board = copy.deepcopy(board)
            make_move(new_board, player, move)
            best_move = Min_Max(new_board, player, False)
            
            best_move = move

        return best_move
    else:
        best_move = None
        for move in valid_moves:
            new_board = copy.deepcopy(board)
            make_move(new_board, -player, move)
            best_move = Min_Max(new_board, player, True)

            best_move = move
                
        return best_move

def get_min_max_move(board, player):
    valid_moves = get_valid_moves(board, player)

    if len(valid_moves) > 0:
        best_move= Min_Max(board, player, False)
        print(best_move)
        if best_move == 0:
            return get_valid_moves(board, player)[0]
        else:
            return best_move
    else:
        return (-1, -1)

def play_othello_vs_AI():
    board = initialize_board()
    current_player = BLACK
    while True:
        print_board(board)
        print("Actual player:", "X" if current_player == BLACK else "O")
        
        if current_player == WHITE:
            row, col = get_min_max_move(board, current_player)
            if row == -1 and col == -1:
                print("O HAS NO MOVEMENTS")
                current_player = -current_player
                continue
        else:
            while True:
                try: 
                    print("mis movs",get_valid_moves(board,current_player))
                    row = int(input("ROW: "))
                    col = int(input("COLUMN: "))
                    if get_valid_moves(board,current_player) == []:
                        current_player = -current_player
                        continue
                    if is_valid_move(get_valid_moves(board,current_player), (row,col)):
                        break
                    else:
                        if len(get_valid_moves(board,current_player)) == 0:
                            current_player = -current_player
                            continue
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Invalid entry. Enter valid numbers.")
        
        make_move(board, current_player, (row,col))
        current_player = -current_player
        
        if terminal_test(board):
            print_board(board)
            black_score, white_score = get_score(board)
            print("States: ", COUNTER)
            if black_score > white_score:
                print("X Won.")
            elif white_score > black_score:
                print("O Won.")
            else:
                print("Tie.")
            break

if __name__ == "__main__":
    opcion = 0
    print(" PLAYER VS IA")
    play_othello_vs_AI()