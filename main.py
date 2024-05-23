import pygame
import sys
from chess_logic import is_valid_move, starting_board, draw_board, draw_pieces, game_over, get_best_move

pygame.init()

WIDTH, HEIGHT = 512, 512
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

def main():
    running = True
    selected_square = None
    last_move = (None, None) 
    turn = 'w'
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
        
        if turn == 'b':
            best_move = get_best_move(starting_board, turn)
            if best_move is not None:
                selected_square, target_square = best_move
                piece = starting_board[selected_square[0]][selected_square[1]]
                starting_board[target_square[0]][target_square[1]] = piece
                starting_board[selected_square[0]][selected_square[1]] = '--'
                last_move = (selected_square, target_square)
                turn = 'w'
            else:
                print("Black has no legal moves left.")
                break

        draw_board()
        draw_pieces(starting_board, selected_square, last_move)
        pygame.display.flip()

        winner, reason = game_over(starting_board, turn)
        if winner:
            print(f"The game is over! {winner} wins by {reason}.")
            running = False

        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()