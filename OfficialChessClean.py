import math
import copy
import time
import argparse

class MiniChess:
    
    def __init__(self):
        self.current_game_state = self.init_board()     
        self.turns_since_capture = 0                    
        self.previous_piece_count = self.count_pieces()

    #Intialize board
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
    
    #Displaying the game board
    def display_board(self, game_state):     
        print()
        for i, row in enumerate (game_state["board"], start =1):       
            print(str(6-i) + "  " + ' '.join(piece.rjust(3) for piece in row))   
        print()
        print("     A   B   C   D   E")
        print()

    # Check if move is in list of valid moves
    def is_valid_move(self, game_state, move):  
        
        start = move[0]  
        end = move[1]  
        start_row, start_col = start 
        end_row, end_col = end 
        board = game_state["board"] 
        turn = game_state ["turn"] 
        
        if (0 <=start_row < 5 and 0 <= start_col <5):
            piece = board[start_row][start_col]  
        else:
            return False
        
        if (0 <=end_row < 5 and 0 <= end_col <5):
            target_piece = board[end_row][end_col]  
        else:
            return False 


        # Ensuring the piece belongs to the current player's turn
        if (turn == 'white' and piece[0] !='w') or (turn == 'black' and piece[0] !='b'):
            return False
        # Ensuring the target position is not occupied by the same player's piece
        if (target_piece != '.' and target_piece[0] == piece[0]):
            return False
        #Ensuring that the empty squares are always valid
        if target_piece =='.':
            return True

        # pieceType is either K,Q,B,N,p
        piece_Type = piece[1]

        #This whole section will determine that allowed moves of each chess pieces
        
        #Implementing all the allowed moves for each piece_Type
        if (piece_Type == 'K'):
            return abs(start_row - end_row) <=1 and abs(start_col - end_col) <=1  
        elif (piece_Type =='Q'):
            if start_row == end_row or start_col == end_col or abs(start_row - end_row) == abs(start_col - end_col): 
                return self.is_path_clear (game_state,move)  
        elif (piece_Type =='B'):
            if abs(start_row - end_row) == abs(start_col - end_col):
                return self.is_path_clear(game_state,move)  
        elif (piece_Type =='N'):
            return (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)] 
        elif (piece_Type =='p'):
            if (piece[0]=='w'):  
                direction = -1   
            else:
                direction = 1 

            # Normal forward move
            if end_col == start_col and end_row == start_row + direction and board[end_row][end_col] == '.':
                return True
            #Capturing a piece diagonally
            if abs(end_col - start_col) == 1 and end_row == start_row + direction and target_piece != '.' and target_piece[0] != piece[0]:
                return True
            # Pawn reaching the end becoming Queen
            #if (piece[0] =='w' and end_row ==0) or (piece[0] =='b' and end_row ==4):
                #return True

        return False
    

    def is_path_clear(self, game_state, move):    

        #Getting the position of the start piece and it's desire end position
        start = move[0]  
        end = move[1]  
        start_row, start_col = start 
        end_row, end_col = end 
        board = game_state["board"]  
        
        # Determine row step
        if start_row == end_row:
            row_step =0            
        elif end_row > start_row:
            row_step = 1           
        else:
            row_step= -1           

        #Determine column step
        if start_col == end_col:
            col_step = 0           
        elif end_col > start_col:
            col_step = 1            
        else:
            col_step = -1           

        #Assigning the row,col
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

        for r in range (5):  
            for c in range (5):   
                piece = board [r][c]

                # Skipping all of the empty squares
                if piece == '.':   
                    continue

                #Ensure the piece belongs to the current player
                if (turn == 'white' and piece[0] != 'w') or (turn == 'black' and piece[0] != 'b'):
                    continue

                #Generate all possible moves based on a piece type
                possible_moves = self.get_piece_moves (game_state, piece, (r,c))

                #Check if the generated moves are valid
                for move in possible_moves:
                    if self.is_valid_move(game_state, move):
                        moves.append(move)

        return moves

    def get_piece_moves(self, game_state, piece, position):
        
        moves = []                        
        start_row, start_col = position   
        board = game_state["board"]       
        piece_type = piece[1]             

        if piece_type == 'K':               
            for dr in [-1, 0, 1]:            
                for dc in [-1, 0, 1]:     
                    if dr == 0 and dc == 0:   
                        continue
                    end = (start_row + dr, start_col + dc)   
                    if 0 <= end[0] < 5 and 0 <= end[1] < 5:  
                        moves.append((position, end))

        elif piece_type == 'Q':  # Checks if Queen could move in any direction
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
            for dr, dc in directions:
                for step in range(1, 5):   
                    end = (start_row + dr * step, start_col + dc * step)
                    if 0 <= end[0] < 5 and 0 <= end[1] < 5:
                        moves.append((position, end))
                        if board[end[0]][end[1]] != '.':  
                            break

        elif piece_type == 'B':  # Bishop moves diagonally
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                for step in range(1, 5):  
                    end = (start_row + dr * step, start_col + dc * step)
                    if 0 <= end[0] < 5 and 0 <= end[1] < 5:
                        moves.append((position, end))
                        if board[end[0]][end[1]] != '.': 
                            break

        elif piece_type == 'N':  # Knight moves in an L-shape
            knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
            for dr, dc in knight_moves:
                end = (start_row + dr, start_col + dc)
                if 0 <= end[0] < 5 and 0 <= end[1] < 5:
                    moves.append((position, end))

        elif piece_type == 'p':  # Pawn moves forward and captures diagonally
            if piece[0] =='w':
                direction =-1
            else:
                direction =1

            # Forward move (one square)
            end = (start_row + direction, start_col)
            if 0 <= end[0] < 5 and board[end[0]][end[1]] == '.':  # Pawn can move forward only if the space is empty
                moves.append((position, end))

            # Capture moves (diagonal left and right)
            for dc in [-1, 1]:  # Diagonal captures
                end = (start_row + direction, start_col + dc)
                if 0 <= end[0] < 5 and 0 <= end[1] < 5:
                    target_piece = board[end[0]][end[1]]
                    if target_piece != '.' and target_piece[0] != piece[0]:  # Must be an opponent's piece
                        moves.append((position, end))

            # Pawn Promotion (Handled separately in `make_move`)
            if (piece[0] == 'w' and start_row == 1) or (piece[0] == 'b' and start_row == 3):
                promotion_square = (start_row + direction, start_col)
                if 0 <= promotion_square[0] < 5 and board[promotion_square[0]][promotion_square[1]] == '.':
                    moves.append((position, promotion_square))  # Pawn reaching promotion square

        return moves


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
        if piece [1] == 'p':
            if (piece[0] =='w' and end_row ==0) or (piece[0] =='b' and end_row ==4):   
                print(f"Pawn promoted to Queen at {chr(end_col + ord('A'))}{5- end_row}") 
                game_state["board"][end_row][end_col]  = piece[0] +'Q'

        #Checking if a piece was captured
        current_piece_count = self.count_pieces()
        if current_piece_count < self.previous_piece_count:  # A piece was captured
            self.turns_since_capture = 0  # Reset draw counter
            self.previous_piece_count = current_piece_count  # Update piece count
        else:
            if game_state["turn"] =="black":
                self.turns_since_capture += 1  # Increase draw counter


        # Updates the turn of the player
        if game_state["turn"] == "white":
            game_state["turn"] ="black"
        else:
            game_state["turn"] = "white"
        
        return game_state
    
    #Counting the number of pieces in the board
    def count_pieces(self):
        
        board = self.current_game_state["board"]
        piece_count = 0
        for row in board:
            for piece in row:
                if piece != '.':
                    piece_count +=1

        return piece_count

    def parse_input(self, move):
        try:
            start, end = move.split()  
            start = (5-int(start[1]), ord(start[0].upper()) - ord('A'))  
            end = (5-int(end[1]), ord(end[0].upper()) - ord('A'))
            return (start, end)
           
        except(ValueError, IndexError):
            print("Invalid input format. Please enter moves in the format 'B2 B3'.")
            return None
        
    def change_to_chess_notation(self, move):
        start, end = move
        start_row, start_col = start
        end_row, end_col = end

        start_position = f"{chr(start_col + ord('A'))}{5 - start_row}"
        end_position = f"{chr(end_col + ord('A'))}{5 - end_row}"
    
        return f"{start_position} {end_position}"
    
    def play(self):   
        
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.") 
        
        while True:  
            
            self.display_board(self.current_game_state)   
            
            moves = self.valid_moves(self.current_game_state)  
            
            # Print moves since last capture for debugging
            print(f"Moves since last capture: {self.turns_since_capture}/10")
            #Converting all moves to chess notation
            converted_moves = [self.change_to_chess_notation(move) for move in moves]
            print (f"Valid Moves for {self.current_game_state['turn'].capitalize()}: {converted_moves}")
           
           
           # Check for game over conditions
            flat_board = [piece for row in self.current_game_state["board"] for piece in row]
            if 'bK' not in flat_board:
                print("White is the winner! The opponent's King was captured. Congradulations!")
                break
            elif 'wK' not in flat_board:
                print("Black is the winner! The opponent's King was captured. Congradulations!")
                break 
            
            if not moves:
                print(f"No valid moves left for {self.current_game_state['turn']}. Game over!")
                exit(0)
            
             # Check for draw condition
            if self.turns_since_capture >= 10:
                print("Game Drawn! No captures in 10 turns.")
                break
            
            move = input(f"{self.current_game_state['turn'].capitalize()} to move: ") 
            
            
            if move.lower() == 'exit':
                print("Game exited.")
                exit(1)
            
            
            move = self.parse_input(move) 
            if not move or not self.is_valid_move(self.current_game_state, move): 
                print("Invalid move. Try again.")
                continue
            
            self.make_move(self.current_game_state, move) 


if __name__ == "__main__":   # Running the game
    game = MiniChess()
    game.play()
