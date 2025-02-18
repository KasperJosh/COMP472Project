import math
import copy
import time
import argparse

class MiniChess:
    def __init__(self):
        self.current_game_state = self.init_board()

    """
    Initialize the board

    Args:
        - None
    Returns:
        - state: A dictionary representing the state of the game
    """
    def init_board(self):
        state = {
                "board": 
                [['bK', 'bQ', 'bB', 'bN', '.'],
                ['.', '.', 'bp', 'bp', '.'],
                ['.', '.', '.', '.', '.'],
                ['.', 'wp', 'wp', '.', '.'],
                ['.', 'wN', 'wB', 'wQ', 'wK']],
                "turn": 'white',
                "draw_counter": 0  # Counter for draw condition
                }
        return state

    """
    Prints the board
    
    Args:
        - game_state: Dictionary representing the current game state
    Returns:
        - None
    """
    def display_board(self, game_state):
        print()
        for i, row in enumerate(game_state["board"], start=1):
            print(str(6-i) + "  " + ' '.join(piece.rjust(3) for piece in row))
        print()
        print("     A   B   C   D   E")
        print()

    """
    Check if the move is valid    
    
    Args: 
        - game_state:   dictionary | Dictionary representing the current game state
        - move          tuple | the move which we check the validity of ((start_row, start_col),(end_row, end_col))
    Returns:
        - boolean representing the validity of the move
    """
    def is_valid_move(self, game_state, move):
        start, end = move
        start_row, start_col = start
        end_row, end_col = end
        board = game_state["board"]
        turn = game_state["turn"]

        piece = board[start_row][start_col]
        target_piece = board[end_row][end_col]

        # Ensure a piece is selected
        if piece == '.':
            return False

        # Ensure the piece belongs to the current player
        if (turn == 'white' and piece[0] != 'w') or (turn == 'black' and piece[0] != 'b'):
            return False

        # Ensure the target square is not occupied by the same player's piece
        if target_piece != '.' and target_piece[0] == piece[0]:
            return False

        piece_type = piece[1]

        if piece_type == 'K':  # King: One square in any direction
            if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
                return True

        elif piece_type == 'Q':  # Queen: Moves like a Rook or Bishop
            if start_row == end_row or start_col == end_col or abs(start_row - end_row) == abs(start_col - end_col):
                return self.is_path_clear(board, start, end)

        elif piece_type == 'B':  # Bishop: Moves diagonally
            if abs(start_row - end_row) == abs(start_col - end_col):
                return self.is_path_clear(board, start, end)

        elif piece_type == 'N':  # Knight: Moves in an L-shape
            if (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)]:
                return True

        elif piece_type == 'p':  # Pawn: Moves forward, captures diagonally
            direction = -1 if piece[0] == 'w' else 1  # White moves up (-1), Black moves down (+1)

            # Normal forward move
            if end_col == start_col and end_row == start_row + direction and board[end_row][end_col] == '.':
                return True

            # Capture diagonally
            if abs(end_col - start_col) == 1 and end_row == start_row + direction and target_piece != '.' and target_piece[0] != piece[0]:
                return True

            # Pawn promotion (handled in `make_move`)
            if (piece[0] == 'w' and end_row == 0) or (piece[0] == 'b' and end_row == 4):
                return True

        return False

    def is_path_clear(self, board, start, end):
        """Helper function to check if path is clear for sliding pieces."""
        start_row, start_col = start
        end_row, end_col = end

        row_step = 0 if start_row == end_row else (1 if end_row > start_row else -1)
        col_step = 0 if start_col == end_col else (1 if end_col > start_col else -1)

        row, col = start_row + row_step, start_col + col_step

        while (row, col) != (end_row, end_col):
            if board[row][col] != '.':
                return False
            row += row_step
            col += col_step

        return True

    """
    Returns a list of valid moves

    Args:
        - game_state: dictionary | Dictionary representing the current game state
    Returns:
        - valid moves: list | A list of nested tuples corresponding to valid moves
    """
    def valid_moves(self, game_state):
        # Return a list of all the valid moves for the current player.
        moves = []
        for r in range(5):
            for c in range(5):
                piece = game_state["board"][r][c]
                if piece != '.' and ((game_state["turn"] == 'white' and piece[0] == 'w') or (game_state["turn"] == 'black' and piece[0] == 'b')):
                    for dr in range(-2, 3):
                        for dc in range(-2, 3):
                            if dr != 0 or dc != 0:
                                move = ((r, c), (r + dr, c + dc))
                                if 0 <= move[1][0] < 5 and 0 <= move[1][1] < 5 and self.is_valid_move(game_state, move):
                                    moves.append(move)
        return moves

    """
    Modify the board to make a move

    Args: 
        - game_state: dictionary | Dictionary representing the current game state
        - move       tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    Returns:
        - game_state: dictionary | Dictionary representing the modified game state
    """
    def make_move(self, game_state, move):
        start, end = move
        start_row, start_col = start
        end_row, end_col = end
        board = game_state["board"]
        piece = board[start_row][start_col]
        target_piece = board[end_row][end_col]

        # Move the piece
        board[start_row][start_col] = '.'
        board[end_row][end_col] = piece

        # Check if the move captures the opponent's King (Win Condition)
        if target_piece != '.' and len(target_piece) > 1 and target_piece[1] == 'K':
            print(f"{game_state['turn'].capitalize()} wins! The opponent's King was captured.")
            exit(0)

        # Pawn Promotion
        if piece[1] == 'p':
            if (piece[0] == 'w' and end_row == 0) or (piece[0] == 'b' and end_row == 4):
                print(f"Pawn promoted to Queen at {chr(end_col + ord('A'))}{5 - end_row}!")
                board[end_row][end_col] = piece[0] + 'Q'

        # Update turn
        game_state["turn"] = "black" if game_state["turn"] == "white" else "white"

        return game_state



    """
    Parse the input string and modify it into board coordinates

    Args:
        - move: string representing a move "B2 B3"
    Returns:
        - (start, end) tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    """
    def parse_input(self, move):
        try:
            start, end = move.split()
            start = (5 - int(start[1]), ord(start[0].upper()) - ord('A'))
            end = (5 - int(end[1]), ord(end[0].upper()) - ord('A'))
            return (start, end)
        except:
            return None

    """
    Game loop

    Args:
        - None
    Returns:
        - None
    """
    def play(self):
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.")
        while True:
            self.display_board(self.current_game_state)
            move = input(f"{self.current_game_state['turn'].capitalize()} to move: ")
            if move.lower() == 'exit':
                print("Game exited.")
                exit(1)

            move = self.parse_input(move)
            if not move or not self.is_valid_move(self.current_game_state, move):
                print("Invalid move. Try again.")
                continue

            self.make_move(self.current_game_state, move)

if __name__ == "__main__":
    game = MiniChess()
    game.play()
