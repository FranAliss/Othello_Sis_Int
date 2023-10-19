import copy

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


def heuristic_weak(board, player):
    black_score, white_score = get_score(board)
    if player == BLACK:
        return black_score - white_score
    else:
        return white_score - black_score


def Min_Max_Alpha_Beta_Heuristic_Pruning(board, depth, player, alpha, beta, maximizing_player):
    if depth == 0 or terminal_test(board):
        return heuristic_weak(board, player), 0
    
    valid_moves = get_valid_moves(board, player)
    if maximizing_player:
        max_val = float('-inf')
        best_move = None
        for move in valid_moves:
            new_board = copy.deepcopy(board)
            make_move(new_board, player, move)
            evaluation, best_move = Min_Max_Alpha_Beta_Heuristic_Pruning(new_board, depth - 1, player, alpha, beta, False)
            
            if evaluation > max_val:
                max_val = evaluation
                best_move = move

            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_val, best_move
    else:
        min_val = float('inf')
        best_move = None
        for move in valid_moves:
            new_board = copy.deepcopy(board)
            make_move(new_board, -player, move)
            evaluation, best_move = Min_Max_Alpha_Beta_Heuristic_Pruning(new_board, depth - 1, player, alpha, beta, True)

            if evaluation < min_val:
                min_val = evaluation
                best_move = move

            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_val, best_move


def get_min_max_move(board, player, depth):
    valid_moves = get_valid_moves(board, player)

    if len(valid_moves) > 0:
        eval, best_move = Min_Max_Alpha_Beta_Heuristic_Pruning(board, depth, player, float('-inf'), float('inf'), False)
        return best_move
    else:
        return None, 
    

def play_othello_vs_AI():
    board = initialize_board()
    current_player = BLACK
    while True:
        print_board(board)
        print("Jugador actual:", "X" if current_player == BLACK else "O")
        
        if current_player == WHITE:
            row, col = get_min_max_move(board, current_player, 5)
            if row == -1 and col == -1:
                current_player = -current_player
                continue
        else:
            while True:
                try:
                    row = int(input("Fila: "))
                    col = int(input("Columna: "))
                    if is_valid_move(get_valid_moves(board,current_player), (row,col)):
                        break
                    else:
                        if len(get_valid_moves(board,current_player)) > 0:
                            current_player = -current_player
                            continue
                        print("Movimiento no válido. Inténtalo de nuevo.")
                except ValueError:
                    print("Entrada no válida. Introduce números válidos.")
        
        make_move(board, current_player, (row,col))
        current_player = -current_player
        
        if terminal_test(board):
            print_board(board)
            black_score, white_score = get_score(board)
            if black_score > white_score:
                print("Negras ganan.")
            elif white_score > black_score:
                print("Blancas ganan.")
            else:
                print("Empate.")
            break

def play_othello_vs_player():
    board = initialize_board()
    current_player = BLACK
    while True:
        print_board(board)
        print("Jugador actual:", "X" if current_player == BLACK else "O")
        
        if current_player == BLACK:
            while True:
                try:
                    row = int(input("Fila: "))
                    col = int(input("Columna: "))
                    if is_valid_move(get_valid_moves(board,current_player), (row,col)):
                        break
                    else:
                        if len(get_valid_moves(board,current_player)) > 0:
                            current_player = -current_player
                            continue
                        print("Movimiento no válido. Inténtalo de nuevo.")
                except ValueError:
                    print("Entrada no válida. Introduce números válidos.")
            make_move(board, current_player, (row,col))
            current_player = -current_player
        else:
            while True:
                try:
                    row = int(input("Fila: "))
                    col = int(input("Columna: "))
                    if is_valid_move(get_valid_moves(board,current_player), (row,col)):
                        break
                    else:
                        if len(get_valid_moves(board,current_player)) > 0:
                            current_player = -current_player
                            continue
                        print("Movimiento no válido. Inténtalo de nuevo.")
                except ValueError:
                    print("Entrada no válida. Introduce números válidos.")
            make_move(board, current_player, (row,col))
            current_player = -current_player
        
        if terminal_test(board):
            print_board(board)
            black_score, white_score = get_score(board)
            if black_score > white_score:
                print("Negras ganan.")
            elif white_score > black_score:
                print("Blancas ganan.")
            else:
                print("Empate.")
                break


if __name__ == "__main__":
    opcion = 0
    print("1. PLAYER VS IA")
    print("2. PLAYER VS PLAYER")
    opcion = int(input("Seleccione el modo de juego: "))
    if opcion == 1:
        play_othello_vs_AI()
    else:
        play_othello_vs_player()