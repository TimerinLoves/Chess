import pygame
import sys
from chess_logic import is_valid_move

pygame.init()

WIDTH, HEIGHT = 512, 512
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

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



def main():
    running = True
    selected_square = None
    last_move = (None, None)  # Initialize last move
    turn = 'w'  # 'w' for white's turn, 'b' for black's turn
    en_passant_target = None
    castling_rights = {(0, 4): ['k', 'q'], (7, 4): ['K', 'Q']}
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = y // 64, x // 64
                if selected_square:
                    selected_row, selected_col = selected_square
                    if is_valid_move(starting_board, selected_square, (row, col), en_passant_target, castling_rights) and starting_board[selected_row][selected_col][0] == turn:
                        piece = starting_board[selected_row][selected_col]
                        target_piece = starting_board[row][col]
                        if piece[1] == 'p' and (row, col) == en_passant_target:
                            if piece[0] == 'w':
                                starting_board[row + 1][col] = '--'
                            else:
                                starting_board[row - 1][col] = '--'
                        starting_board[row][col] = starting_board[selected_row][selected_col]
                        starting_board[selected_row][selected_col] = '--'
                        last_move = (selected_square, (row, col))
                        selected_square = None
                        en_passant_target = None
                        if piece[1] == 'p' and abs(selected_row - row) == 2:
                            en_passant_target = (row + (1 if piece[0] == 'w' else -1), col)
                        if piece[1] == 'k' and abs(selected_col - col) == 2:
                            if col > selected_col:
                                starting_board[row][col - 1] = starting_board[row][7]
                                starting_board[row][7] = '--'
                            else:
                                starting_board[row][col + 1] = starting_board[row][0]
                                starting_board[row][0] = '--'
                            castling_rights[(row, col)] = []
                        if piece[1] in ['k', 'r']:
                            castling_rights[(selected_row, selected_col)] = []
                        turn = 'b' if turn == 'w' else 'w'
                    else:
                        selected_square = (row, col)
                else:
                    selected_square = (row, col)

        draw_board()
        draw_pieces(starting_board, selected_square, last_move)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()