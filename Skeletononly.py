import math  # Imports the Python math module
import copy  # Imports the copy module, which allow deep and shallow copying of objects
import time #Handles time-related functions (sleep, timestamps, etc)
import argparse  #Used for parsing commend line arguments

class MiniChess: 
    def __init__(self):   #Constructor in Python that initializes an object when a class is instantiated
        
        #
        self.current_game_state = self.init_board() # Method inside the class that returns the initial board setup. Starts a fresh game board

    """
    Initialize the board

    Args:
        - None
    Returns:
        - state: A dictionary representing the state of the game
    """
    def init_board(self):
        state = {       #Creates a dictionary call state
                "board": # Stores the game board as a 2D list
                [['bK', 'bQ', 'bB', 'bN', '.'],
                ['.', '.', 'bp', 'bp', '.'],
                ['.', '.', '.', '.', '.'],
                ['.', 'wp', 'wp', '.', '.'],
                ['.', 'wN', 'wB', 'wQ', 'wK']],
                "turn": 'white',
                }
        return state

    """
    Prints the board
    
    Args:
        - game_state: Dictionary representing the current game state
    Returns:
        - None
    """
    def display_board(self, game_state):    # self refers to the instance of the class game_state is a dictionary that contains the board and turn information
        print()
        for i, row in enumerate(game_state["board"], start=1):
            print(str(6-i) + "  " + ' '.join(piece.rjust(3) for piece in row))
            #The board is 5x5, so we number rows from top(5) to bottom(1)
            #str(6-i) + " " → Adds row number with spacing
            #piece.rjust(3) ensures each piece is right-aligned within 3 spaces
            # 
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
        # Check if move is in list of valid moves
        return True

    """
    Returns a list of valid moves

    Args:
        - game_state:   dictionary | Dictionary representing the current game state
    Returns:
        - valid moves:   list | A list of nested tuples corresponding to valid moves [((start_row, start_col),(end_row, end_col)),((start_row, start_col),(end_row, end_col))]
    """
    def valid_moves(self, game_state):
        # Return a list of all the valid moves.
        # Implement basic move validation
        # Check for out-of-bounds, correct turn, move legality, etc
        return

    """
    Modify to board to make a move

    Args: 
        - game_state:   dictionary | Dictionary representing the current game state
        - move          tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    Returns:
        - game_state:   dictionary | Dictionary representing the modified game state
    """
    def make_move(self, game_state, move):
        start = move[0]  # Basically where the start piece is, #(start_row, start_col)
        end = move[1]  # The The end move piece
        start_row, start_col = start # Starting position is unpacked into start_row, start_col
        end_row, end_col = end # Ending position is unplacked into end_row, end_col
        piece = game_state["board"][start_row][start_col]  # Finds the piece at the starting position
        # Example move = ((4, 3), (3, 3))  # Moving White Queen from (4,3) to (3,3)
        # piece = "wQ"
        game_state["board"][start_row][start_col] = '.'  #clearing the starting posiition after moving the piece
        game_state["board"][end_row][end_col] = piece  #Places the piece at the new position
        #game_state["board"][3][3] = "wQ"  # White Queen moves to (3,3)
        game_state["turn"] = "black" if game_state["turn"] == "white" else "white"
        # Switches the turn between "white" and "black".
        return game_state

    """
    Parse the input string and modify it into board coordinates

    Args:
        - move: string representing a move "B2 B3"
    Returns:
        - (start, end)  tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    """
    def parse_input(self, move):
        try:
            start, end = move.split()
            start = (5-int(start[1]), ord(start[0].upper()) - ord('A'))
            end = (5-int(end[1]), ord(end[0].upper()) - ord('A'))
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