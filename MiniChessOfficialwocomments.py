import math
import copy
import time
import argparse

class MiniChess:
    
    def __init__(self):
        self.current_game_state = self.init_board()  # Initializing the game with the starting board 
        self.turns_since_capture = 0   # Tracking the moves since last cpature to check for draws                   
        self.previous_piece_count = self.count_pieces()  # Storing the initial count of pieces
        self.moves_number = 1  # Track the turn number
        self.trace_file = open("gameTrace.txt", "w")  # Opening the trace file for writing the moves

    # Initialize board
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
    
    # Displaying the current state of the game board
    def display_board(self, game_state):     
        print()
        for i, row in enumerate(game_state["board"], start=1):       
            print(str(6 - i) + "  " + ' '.join(piece.rjust(3) for piece in row))   
        print()
        print("     A   B   C   D   E")
        print()

    # Check if move is valid for the current game state
    def is_valid_move(self, game_state, move):  
        start = move[0]  # Starting position of the move
        end = move[1]  # Ending position of the move
        start_row, start_col = start 
        end_row, end_col = end 
        board = game_state["board"] 
        turn = game_state["turn"] 
        
        # Check if start and end positions are within the board boundaries
        if not (0 <= start_row < 5 and 0 <= start_col < 5):
            return False
        if not (0 <= end_row < 5 and 0 <= end_col < 5):
            return False 

        piece = board[start_row][start_col]    # Initializing the piece being moved
        target_piece = board[end_row][end_col]  # Initializing the piece at the target position

        # Ensure the piece belongs to the current player's turn
        if (turn == 'white' and piece[0] != 'w') or (turn == 'black' and piece[0] != 'b'):
            return False

        # Ensure the target position is not occupied by the same player's piece
        if target_piece != '.' and target_piece[0] == piece[0]:
            return False

        # pieceType is either K, Q, B, N, p
        piece_type = piece[1]

        # Implementing all the movement rules for each piece type
        if piece_type == 'K':  # King
            return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1  
        elif piece_type == 'Q':  # Queen
            if start_row == end_row or start_col == end_col or abs(start_row - end_row) == abs(start_col - end_col): 
                return self.is_path_clear(game_state, move)  
        elif piece_type == 'B':  # Bishop
            if abs(start_row - end_row) == abs(start_col - end_col):
                return self.is_path_clear(game_state, move)  
        elif piece_type == 'N':  # Knight
            return (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)] 
        elif piece_type == 'p':  # Pawn
            if piece[0] == 'w':  # White pawn
                direction = -1  # Moves upward
            else:  # Black pawn
                direction = 1  # Moves downward

            # Normal forward move
            if end_col == start_col and end_row == start_row + direction and target_piece == '.':
                return True
            # Capturing a piece diagonally
            if abs(end_col - start_col) == 1 and end_row == start_row + direction and target_piece != '.' and target_piece[0] != piece[0]:
                return True
        else:
            return False
    
    def is_path_clear(self, game_state, move):    
        start = move[0]  
        end = move[1]  
        start_row, start_col = start 
        end_row, end_col = end 
        board = game_state["board"]  
        
        # Determine row step
        if start_row == end_row:
            row_step = 0            
        elif end_row > start_row:
            row_step = 1           
        else:
            row_step = -1           

        # Determine column step
        if start_col == end_col:
            col_step = 0           
        elif end_col > start_col:
            col_step = 1            
        else:
            col_step = -1           

        # Assigning the row,col
        row, col = start_row + row_step, start_col + col_step   

        while (row, col) != (end_row, end_col):  
            if board[row][col] != '.':           
                return False                     
            row += row_step                      
            col += col_step                      

        return True
    
    def valid_moves(self, game_state):
        moves = []                     
        board = game_state["board"]    
        turn = game_state["turn"]      

        for row in range(5):  
            for col in range(5):   
                piece = board[row][col]

                # Skip empty squares
                if piece == '.':   
                    continue
                # Ensure the piece belongs to the current player
                if (turn == 'white' and piece[0] == 'w') or (turn == 'black' and piece[0] == 'b'):
                    for r in range(5):
                        for c in range(5):
                            move = ((row, col), (r, c))
                            if self.is_valid_move(game_state, move):
                                moves.append(move)

        return moves
    
    # Print all possible moves for the current player
    def print_possible_moves(self, game_state):
        
        valid_moves =[]
        moves = self.valid_moves(game_state)
        print(f"Possible moves for {game_state['turn'].capitalize()}:")
        for move in moves:
            start, end = move
            start_row, start_col = start
            end_row, end_col = end
            start_pos = f"{chr(start_col + ord('A'))}{5 - start_row}"
            end_pos = f"{chr(end_col + ord('A'))}{5 - end_row}"
            valid_moves.append(f"'{start_pos} {end_pos}'")
        print(", ".join(valid_moves))


    def make_move(self, game_state, move):
        start = move[0]  
        end = move[1] 
        start_row, start_col = start 
        end_row, end_col = end 
        piece = game_state["board"][start_row][start_col]  
        target_piece = game_state["board"][end_row][end_col] 
        
        game_state["board"][start_row][start_col] = '.'  
        game_state["board"][end_row][end_col] = piece  
        
        # Promoting pawn to Queen
        if piece[1] == 'p':
            if (piece[0] == 'w' and end_row == 0) or (piece[0] == 'b' and end_row == 4):   
                print(f"Pawn promoted to Queen at {chr(end_col + ord('A'))}{5 - end_row}") 
                game_state["board"][end_row][end_col] = piece[0] + 'Q'

        # Log the action to the trace file
        self.log_action(game_state, move)

        # Checking if a piece was captured
        current_piece_count = self.count_pieces()
        if current_piece_count < self.previous_piece_count:  # A piece was captured
            self.turns_since_capture = 0  # Reset draw counter
            self.previous_piece_count = current_piece_count  # Update piece count
        else:
            if self.moves_number % 2 ==0:
                self.turns_since_capture += 1  # Increase draw counter

        # Updates the turn of the player
        if game_state["turn"] == "white":
            game_state["turn"] = "black"
        else:
            game_state["turn"] = "white"
        
        self.moves_number += 1  # Increment the turn number
        
        return game_state
    
    # Log the action to the trace file
    def log_action(self, game_state, move):
        start = move[0]  
        end = move[1] 
        start_row, start_col = start 
        end_row, end_col = end 
        piece = game_state["board"][end_row][end_col]  # Piece after the move

        # Convert coordinates to chess notation (e.g., A1, B2)
        start_pos = f"{chr(start_col + ord('A'))}{5 - start_row}"
        end_pos = f"{chr(end_col + ord('A'))}{5 - end_row}"

        # Write to the trace file
        self.trace_file.write(f"Turn #{(self.moves_number+1)//2}: {game_state['turn'].capitalize()} moves {piece} from {start_pos} to {end_pos}\n")
        self.trace_file.write("Board configuration:\n")
        self.trace_file.write("\n")
        for i, row in enumerate(game_state["board"]):
            self.trace_file.write(f"{5-i}" + "  " + f"{'   '.join(row)}\n")
        self.trace_file.write("     A   B   C   D   E\n")
        self.trace_file.write("\n")



    # Counting the number of pieces in the board
    def count_pieces(self):
        board = self.current_game_state["board"]
        piece_count = 0
        for row in board:
            for piece in row:
                if piece != '.':
                    piece_count += 1

        return piece_count

    def parse_input(self, move):
        
        try:
            start, end = move.split()  
            start = (5 - int(start[1]), ord(start[0].upper()) - ord('A'))  
            end = (5 - int(end[1]), ord(end[0].upper()) - ord('A'))
            return (start, end)
           
        except (ValueError, IndexError):
            print("Invalid input format. Please enter moves in the format 'B2 B3'.")
            return None
    
    def play(self):   
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.") 
        
        while True:  
            self.display_board(self.current_game_state)   
            self.print_possible_moves(self.current_game_state)
            
             # Print turns since last capture for debugging
            print(f"Turns since last capture: {self.turns_since_capture}/10")
            
            # Check for game over conditions
            flat_board = [piece for row in self.current_game_state["board"] for piece in row]
            if 'bK' not in flat_board:
                print("White is the winner! The opponent's King was captured. Congratulations!")
                print(f"White won in {(self.moves_number)//2} turns!")
                self.trace_file.write("White wins! The opponent's King was captured.\n")
                self.trace_file.write(f"White won in {self.moves_number//2} turns!\n")
                break
            elif 'wK' not in flat_board:
                print("Black is the winner! The opponent's King was captured. Congratulations!")
                print(f"Black won in {self.moves_number//2} turns!")
                self.trace_file.write("Black wins! The opponent's King was captured.\n")
                self.trace_file.write(f"Black won in {self.moves_number//2} turns!\n")
                break 
            
            # Check for draw condition
            if self.turns_since_capture >= 10:
                print("Game ended in a Draw! No captures in 10 turns.")
                self.trace_file.write("Game Drawn! No captures in full 10 turns.\n")
                return
            
        
            move = input(f"{self.current_game_state['turn'].capitalize()} to move: ") 
            
            if move.lower() == 'exit':
                print("Game exited.")
                self.trace_file.write("Game exited by the player.\n")
                return
            
            parsed_move = self.parse_input(move) 

            if not parsed_move:
                print("Invalid input format. Please use the format 'B2 B3'.")
                continue
            if not self.is_valid_move(self.current_game_state, parsed_move): 
                print("Illegal move! Move could be out of bounds, occupied by own piece or invalid. Try again!")
                continue
            
            self.make_move(self.current_game_state, parsed_move) 

        self.trace_file.close()  # Close the trace file when the game ends


if __name__ == "__main__":   # Running the game
    game = MiniChess()
    game.play()