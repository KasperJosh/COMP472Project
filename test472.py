import math
import copy
import time
import argparse

class MiniChess:
    def __init__(self):
        self.current_game_state = self.init_board()
        self.no_capture_turns = 0

    def init_board(self):
        state = {
            "board": 
            [['bK', 'bQ', 'bB', 'bN', '.'],
            ['.', '.', 'bp', 'bp', '.'],
            ['.', '.', '.', '.', '.'],
            ['.', 'wp', 'wp', '.', '.'],
            ['.', 'wN', 'wB', 'wQ', 'wK']],
            "turn": 'white',
        }
        return state

    def display_board(self, game_state):
        print()
        for i, row in enumerate(game_state["board"], start=1):
            print(str(6-i) + "  " + ' '.join(piece.rjust(3) for piece in row))
        print()
        print("     A   B   C   D   E")
        print()

    def is_valid_move(self, game_state, move):
        start, end = move
        start_row, start_col = start
        end_row, end_col = end
        board = game_state["board"]
        piece = board[start_row][start_col]

        # Check if it's the correct player's turn
        if (game_state["turn"] == "white" and not piece.startswith('w')) or \
           (game_state["turn"] == "black" and not piece.startswith('b')):
            return False

        # Ensure destination is within bounds
        if not (0 <= end_row < 5 and 0 <= end_col < 5):
            return False

        # Prevent moving onto your own piece
        if board[end_row][end_col] != '.' and board[end_row][end_col][0] == piece[0]:
            return False

        # Implement movement rules for each piece
        if piece[1] == 'K':  # King
            return abs(end_row - start_row) <= 1 and abs(end_col - start_col) <= 1
        elif piece[1] == 'Q':  # Queen
            return self.is_straight_or_diagonal_move(start, end, board)
        elif piece[1] == 'B':  # Bishop
            return self.is_diagonal_move(start, end, board)
        elif piece[1] == 'N':  # Knight
            return (abs(end_row - start_row), abs(end_col - start_col)) in [(2, 1), (1, 2)]
        elif piece[1] == 'p':  # Pawn
            direction = -1 if piece.startswith('w') else 1
            if end_col == start_col:  # Move forward
                return end_row == start_row + direction and board[end_row][end_col] == '.'
            elif abs(end_col - start_col) == 1:  # Capture diagonally
                return end_row == start_row + direction and board[end_row][end_col].startswith('b' if piece.startswith('w') else 'w')
        
        return False

    def is_straight_or_diagonal_move(self, start, end, board):
        start_row, start_col = start
        end_row, end_col = end

        delta_row = end_row - start_row
        delta_col = end_col - start_col

        if delta_row == 0 or delta_col == 0:  # Straight line
            step_row = 0 if delta_row == 0 else delta_row // abs(delta_row)
            step_col = 0 if delta_col == 0 else delta_col // abs(delta_col)
        elif abs(delta_row) == abs(delta_col):  # Diagonal line
            step_row = delta_row // abs(delta_row)
            step_col = delta_col // abs(delta_col)
        else:
            return False

        current_row, current_col = start_row + step_row, start_col + step_col
        while (current_row != end_row or current_col != end_col):
            if board[current_row][current_col] != '.':
                return False
            current_row += step_row
            current_col += step_col
        
        return True

    def is_diagonal_move(self, start, end, board):
        delta_row = abs(end[0] - start[0])
        delta_col = abs(end[1] - start[1])
        
        return delta_row == delta_col and self.is_straight_or_diagonal_move(start, end, board)

    def valid_moves(self, game_state):
        moves = []
        for row in range(5):
            for col in range(5):
                piece = game_state["board"][row][col]
                if (game_state["turn"] == "white" and piece.startswith('w')) or \
                   (game_state["turn"] == "black" and piece.startswith('b')):
                    for r in range(5):
                        for c in range(5):
                            move = ((row, col), (r, c))
                            if self.is_valid_move(game_state, move):
                                moves.append(move)
        return moves

    def make_move(self, game_state, move):
        start, end = move
        start_row, start_col = start
        end_row, end_col = end
        piece = game_state["board"][start_row][start_col]
        game_state["board"][start_row][start_col] = '.'
        game_state["board"][end_row][end_col] = piece

        # Pawn promotion
        if piece[1] == 'p' and (end_row == 0 or end_row == 4):
            game_state["board"][end_row][end_col] = piece[0] + 'Q'

        game_state["turn"] = "black" if game_state["turn"] == "white" else "white"

        return game_state

    def parse_input(self, move):
        try:
            start, end = move.split()
            start = (5-int(start[1]), ord(start[0].upper()) - ord('A'))
            end = (5-int(end[1]), ord(end[0].upper()) - ord('A'))
            return (start, end)
        except:
            return None

    def play(self):
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.")
        
        while True:
            self.display_board(self.current_game_state)
            
            # Check for game over conditions
            flat_board = [piece for row in self.current_game_state["board"] for piece in row]
            if 'bK' not in flat_board:
                print("White wins!")
                break
            elif 'wK' not in flat_board:
                print("Black wins!")
                break
            
            if self.no_capture_turns >= 10:
                print("Draw! No captures in the last 10 turns.")
                break
            
            move = input(f"{self.current_game_state['turn'].capitalize()} to move: ")
            
            if move.lower() == 'exit':
                print("Game exited.")
                exit(1)

            parsed_move = self.parse_input(move)
            
            if not parsed_move or not self.is_valid_move(self.current_game_state, parsed_move):
                print("Invalid move. Try again.")
                continue
            
            # Check if a capture occurs
            _, dest = parsed_move
            dest_piece = self.current_game_state["board"][dest[0]][dest[1]]
            
            self.make_move(self.current_game_state, parsed_move)
            
            self.no_capture_turns = self.no_capture_turns + 1 if dest_piece == '.' else 0

if __name__ == "__main__":
    game = MiniChess()
    game.play()
