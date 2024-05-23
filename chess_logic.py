import pygame
import sys

WIDTH, HEIGHT = 512, 512
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

piece_value = {
    'p': 1,
    'n': 3,
    'b': 3,
    'r': 5,
    'q': 9, 
    'k': 100 
}

starting_board = [
    ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
    ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['--', '--', '--', '--', '--', '--', '--', '--'],
    ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
    ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
]

chessboard_image = pygame.image.load('images/chessboard.png')

pieces = {
    'wp': pygame.image.load('images/white/pawn.png'),
    'wr': pygame.image.load('images/white/rook.png'),
    'wn': pygame.image.load('images/white/knight.png'),
    'wb': pygame.image.load('images/white/bishop.png'),
    'wq': pygame.image.load('images/white/queen.png'),
    'wk': pygame.image.load('images/white/king.png'),
    'bp': pygame.image.load('images/black/pawn.png'),
    'br': pygame.image.load('images/black/rook.png'),
    'bn': pygame.image.load('images/black/knight.png'),
    'bb': pygame.image.load('images/black/bishop.png'),
    'bq': pygame.image.load('images/black/queen.png'),
    'bk': pygame.image.load('images/black/king.png')
}

def game_over(board, turn):
    king_position = find_king(board, turn)
    if is_stalemate(board):
        return None, 'stalemate'
    elif is_checkmate(board, king_position, turn):
        return 'black' if turn == 'w' else 'white', 'checkmate'
    else:
        return None, None
    
def get_best_move(board, turn):
    best_move = None
    best_score = float('-inf')

    for move in generate_moves(board):
        new_board = make_move(board, move)
        score = minimax(new_board, 3, float('-inf'), float('inf'), False, turn)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move

def draw_board():
    WINDOW.blit(chessboard_image, (0, 0))

def draw_pieces(board, selected_square, last_move):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if (row, col) == last_move[0]:
                pygame.draw.rect(WINDOW, (200, 245, 170), (col*64, row*64, 64, 64))
            if (row, col) == last_move[1]:
                pygame.draw.rect(WINDOW, (135, 220, 95), (col*64, row*64, 64, 64))
            if piece != '--':
                if (row, col) == selected_square:
                    pygame.draw.rect(WINDOW, (173, 216, 230), (col*64, row*64, 64, 64))
                WINDOW.blit(pieces[piece], (col*64, row*64))

def minimax(board, depth, alpha, beta, maximizing_player, turn):
    if depth == 0 or game_over(board, turn):
        return evaluate(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in generate_moves(board):
            new_board = make_move(board, move)
            eval = minimax(new_board, depth - 1, alpha, beta, False, 'w' if turn == 'b' else 'b')
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in generate_moves(board):
            new_board = make_move(board, move)
            eval = minimax(new_board, depth - 1, alpha, beta, True, 'w' if turn == 'b' else 'b')
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
    
def evaluate(board):
    score = 0
    for row in board:
        for piece in row:
            if piece.startswith('b'):
                score += piece_value[piece[1]]
            elif piece.startswith('w'):
                score -= piece_value[piece[1]]
    return score

def is_check(board, king_position, enemy_color):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece[0] == enemy_color:
                if is_valid_move(board, (row, col), king_position, None, {}):
                    return True
    return False

def is_checkmate(board, king_position, color):
    if not is_check(board, king_position, 'b' if color == 'w' else 'w'):
        return False
    
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece[0] == color:
                moves = generate_moves(board, (row, col))
                for move in moves:
                    new_board = make_move(board, move)
                    if not is_check(new_board, king_position, 'b' if color == 'w' else 'w'):
                        return False
    return True

def is_stalemate(board):
    for row in range(8):
        for col in range(8):
            if board[row][col].startswith('b'):
                moves = generate_moves(board)
                if moves:
                    return False
    return True


def find_king(board, color):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == color + 'k':
                return row, col
    return None

def generate_moves(board,position):
    moves = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece.startswith('b'):
                moves.extend(get_piece_moves(board, (row, col)))
    return moves

def get_piece_moves(board, position):
    row, col = position
    piece = board[row][col]
    moves = []

    if piece == 'bp':
        if row + 1 < 8 and board[row + 1][col] == '--':
            moves.append(((row, col), (row + 1, col)))
        if row == 1 and board[row + 1][col] == '--' and board[row + 2][col] == '--':
            moves.append(((row, col), (row + 2, col)))
        if row + 1 < 8 and col + 1 < 8 and board[row + 1][col + 1].startswith('w'):
            moves.append(((row, col), (row + 1, col + 1)))
        if row + 1 < 8 and col - 1 >= 0 and board[row + 1][col - 1].startswith('w'):
            moves.append(((row, col), (row + 1, col - 1)))
    elif piece == 'bn':
        knight_moves = [(row - 1, col - 2), (row - 2, col - 1), (row - 2, col + 1),
                        (row - 1, col + 2), (row + 1, col + 2), (row + 2, col + 1),
                        (row + 2, col - 1), (row + 1, col - 2)]
        for move in knight_moves:
            if 0 <= move[0] < 8 and 0 <= move[1] < 8 and (not board[move[0]][move[1]].startswith('b')):
                moves.append(((row, col), move))
    elif piece == 'bb':
        moves.extend(get_diagonal_moves(board, position))
    elif piece == 'br':
        moves.extend(get_straight_moves(board, position))
    elif piece == 'bq':
        moves.extend(get_diagonal_moves(board, position))
        moves.extend(get_straight_moves(board, position))
    elif piece == 'bk':
        king_moves = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                      (row, col - 1), (row, col + 1),
                      (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]
        for move in king_moves:
            if 0 <= move[0] < 8 and 0 <= move[1] < 8 and (not board[move[0]][move[1]].startswith('b')):
                moves.append(((row, col), move))

    return moves

def get_diagonal_moves(board, position):
    row, col = position
    moves = []

    for i in range(1, 8):
        if row - i >= 0 and col + i < 8:
            if board[row - i][col + i] == '--':
                moves.append(((row, col), (row - i, col + i)))
            elif board[row - i][col + i].startswith('w'):
                moves.append(((row, col), (row - i, col + i)))
                break
            else:
                break
        else:
            break

    for i in range(1, 8):
        if row - i >= 0 and col - i >= 0:
            if board[row - i][col - i] == '--':
                moves.append(((row, col), (row - i, col - i)))
            elif board[row - i][col - i].startswith('w'):
                moves.append(((row, col), (row - i, col - i)))
                break
            else:
                break
        else:
            break

    for i in range(1, 8):
        if row + i < 8 and col + i < 8:
            if board[row + i][col + i] == '--':
                moves.append(((row, col), (row + i, col + i)))
            elif board[row + i][col + i].startswith('w'):
                moves.append(((row, col), (row + i, col + i)))
                break
            else:
                break
        else:
            break

    for i in range(1, 8):
        if row + i < 8 and col - i >= 0:
            if board[row + i][col - i] == '--':
                moves.append(((row, col), (row + i, col - i)))
            elif board[row + i][col - i].startswith('w'):
                moves.append(((row, col), (row + i, col - i)))
                break
            else:
                break
        else:
            break

    return moves

def get_straight_moves(board, position):
    row, col = position
    moves = []

    for i in range(col + 1, 8):
        if board[row][i] == '--':
            moves.append(((row, col), (row, i)))
        elif board[row][i].startswith('w'):
            moves.append(((row, col), (row, i)))
            break
        else:
            break

    for i in range(col - 1, -1, -1):
        if board[row][i] == '--':
            moves.append(((row, col), (row, i)))
        elif board[row][i].startswith('w'):
            moves.append(((row, col), (row, i)))
            break
        else:
            break

    for i in range(row - 1, -1, -1):
        if board[i][col] == '--':
            moves.append(((row, col), (i, col)))
        elif board[i][col].startswith('w'):
            moves.append(((row, col), (i, col)))
            break
        else:
            break

    for i in range(row + 1, 8):
        if board[i][col] == '--':
            moves.append(((row, col), (i, col)))
        elif board[i][col].startswith('w'):
            moves.append(((row, col), (i, col)))
            break
        else:
            break

    return moves

def make_move(board, move):
    new_board = [row[:] for row in board]
    (start_row, start_col), (end_row, end_col) = move
    new_board[end_row][end_col] = new_board[start_row][start_col]
    new_board[start_row][start_col] = '--'
    return new_board

def is_valid_move(board, start, end, en_passant_target, castling_rights):
    start_row, start_col = start
    end_row, end_col = end
    piece = board[start_row][start_col]
    if piece == '--':
        return False
    piece_type = piece[1]
    if piece_type == 'p':
        return is_valid_pawn_move(board, start, end, en_passant_target)
    elif piece_type == 'r':
        return is_valid_rook_move(board, start, end)
    elif piece_type == 'n':
        return is_valid_knight_move(board, start, end)
    elif piece_type == 'b':
        return is_valid_bishop_move(board, start, end)
    elif piece_type == 'q':
        return is_valid_queen_move(board, start, end)
    elif piece_type == 'k':
        return is_valid_king_move(board, start, end, castling_rights)
    return False

def is_valid_pawn_move(board, start, end, en_passant_target):
    start_row, start_col = start
    end_row, end_col = end
    piece = board[start_row][start_col]
    if piece[0] == 'w':
        direction = -1
        start_row_pawn = 6
    else:
        direction = 1
        start_row_pawn = 1

    if start_col == end_col:
        if board[end_row][end_col] == '--':
            if start_row + direction == end_row:
                return True
            if start_row == start_row_pawn and start_row + 2 * direction == end_row and board[start_row + direction][start_col] == '--':
                return True
    elif abs(start_col - end_col) == 1 and start_row + direction == end_row:
        if board[end_row][end_col] != '--' and board[end_row][end_col][0] != piece[0]:
            return True
        if (end_row, end_col) == en_passant_target:
            return True
    return False

def is_valid_rook_move(board, start, end):
    return is_straight_move(board, start, end)

def is_valid_knight_move(board, start, end):
    start_row, start_col = start
    end_row, end_col = end
    if (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)]:
        if board[end_row][end_col] == '--' or board[end_row][end_col][0] != board[start_row][start_col][0]:
            return True
    return False

def is_valid_bishop_move(board, start, end):
    return is_diagonal_move(board, start, end)

def is_valid_queen_move(board, start, end):
    return is_straight_move(board, start, end) or is_diagonal_move(board, start, end)

def is_valid_king_move(board, start, end, castling_rights):
    start_row, start_col = start
    end_row, end_col = end
    if max(abs(start_row - end_row), abs(start_col - end_col)) == 1:
        if board[end_row][end_col] == '--' or board[end_row][end_col][0] != board[start_row][start_col][0]:
            return True
    if start_row == end_row and abs(start_col - end_col) == 2:
        if (start_row, start_col) in castling_rights and castling_rights[(start_row, start_col)]:
            rook_col = 0 if end_col < start_col else 7
            if is_clear_path(board, (start_row, start_col), (start_row, rook_col)):
                return True
    return False

def is_straight_move(board, start, end):
    start_row, start_col = start
    end_row, end_col = end
    if start_row != end_row and start_col != end_col:
        return False
    step_row = (end_row - start_row) // max(1, abs(end_row - start_row))
    step_col = (end_col - start_col) // max(1, abs(end_col - start_col))
    for i in range(1, max(abs(end_row - start_row), abs(end_col - start_col))):
        if board[start_row + i * step_row][start_col + i * step_col] != '--':
            return False
    if board[end_row][end_col] == '--' or board[end_row][end_col][0] != board[start_row][start_col][0]:
        return True
    return False

def is_diagonal_move(board, start, end):
    start_row, start_col = start
    end_row, end_col = end
    if abs(start_row - end_row) != abs(start_col - end_col):
        return False
    if abs(start_row - end_row) == 0:
        return False
    step_row = (end_row - start_row) // abs(end_row - start_row)
    step_col = (end_col - start_col) // abs(end_col - start_col)
    for i in range(1, abs(end_row - start_row)):
        if board[start_row + i * step_row][start_col + i * step_col] != '--':
            return False
    if board[end_row][end_col] == '--' or board[end_row][end_col][0] != board[start_row][start_col][0]:
        return True
    return False

def is_clear_path(board, start, end):
    start_row, start_col = start
    end_row, end_col = end
    step_row = (end_row - start_row) // max(1, abs(end_row - start_row))
    step_col = (end_col - start_col) // max(1, abs(end_col - start_col))
    for i in range(1, max(abs(end_row - start_row), abs(end_col - start_col))):
        if board[start_row + i * step_row][start_col + i * step_col] != '--':
            return False
    return True
