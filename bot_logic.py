from chess_logic import starting_board, minimax, make_move, get_best_move, game_over

def play_as_black():
    while True:
        best_move = get_best_move(starting_board, 'b')
        selected_square, target_square = best_move
        piece = starting_board[selected_square[0]][selected_square[1]]
        starting_board[target_square[0]][target_square[1]] = piece
        starting_board[selected_square[0]][selected_square[1]] = '--'
        print(f"Black moves: {selected_square} to {target_square}")
        print_board(starting_board)
        if game_over(starting_board, 'w')[0]:
            print("White wins by checkmate.")
            break

def print_board(board):
    for row in board:
        print(row)
    print()

if __name__ == "__main__":
    play_as_black()
