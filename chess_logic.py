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
