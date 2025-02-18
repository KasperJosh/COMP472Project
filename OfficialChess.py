import math
import copy
import time
import argparse


class MiniChess:
    
    def __init__(self):
        self.current_game_state = self.init_board()     #Initializes the board
        self.moves_since_capture = 0                    #Tracking moves without since the last capture piece
        self.previous_piece_count = self.count_pieces() #Track initial number of pieces

    
    """
    Initialize the board

    Args:
        - None
    Returns:
        - state: A dictionary representing the state of the game
    """
    def init_board(self):
        state = {                                  # Dictionary called state
                "board":                           # Stores the game board as a 2D list
                [['bK', 'bQ', 'bB', 'bN', '.'],    # Row index 0
                ['.', '.', 'bp', 'bp', '.'],       # Row index 1
                ['.', '.', '.', '.', '.'],         # Row index 2
                ['.', 'wp', 'wp', '.', '.'],       # Row index 3
                ['.', 'wN', 'wB', 'wQ', 'wK']],    # Row index 4
                "turn": 'white',                   # White starts the game first
                }
        return state

    
    
    """
    Prints the board
    
    Args:
        - game_state: Dictionary representing the current game state
    Returns:
        - None
    """
    def display_board(self, game_state):     #Displaying the game board
        print()
        for i, row in enumerate (game_state["board"], start =1):       
            print(str(6-i) + "  " + ' '.join(piece.rjust(3) for piece in row))   #Prints example "5   bK  wQ  bB  bN   ."
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
    def is_valid_move(self, game_state, move):  # Check if move is in list of valid moves
        
        #Getting the position of the start piece and it's desire end position
        start = move[0]  # Position of start piece. Ex: Let's take 'wp', start =  B3 (3,1)
        end = move[1]  # Desired end position. Ex: B2 (2,1)
        start_row, start_col = start # start position is unpacked into start_row (3), start_col(1)
        end_row, end_col = end # Ending position is unpacked into end_row (2), end_col (1)
        
        #Extracting the board and turn
        board = game_state["board"]  # Extracts the game board from game_state dictionary, allows modifying board easily
        turn = game_state ["turn"] # Extracts the current player's turn ("white" or "black")
        
        if (0 <=start_row < 5 and 0 <= start_col <5):
            piece = board[start_row][start_col]  #Extracts the piece where you would like to move the piece. Ex: On initial board → board[2][1] = "."
        else:
            return False
                
        if (0 <=end_row < 5 and 0 <= end_col <5):
            target_piece = board[end_row][end_col]  #Extracts the piece where you would like to move the piece. Ex: On initial board → board[2][1] = "."
        else:
            return False

        # Ensuring a piece is selected and not an empty slot
        #if piece == '.':
            #print(f"There is no piece in this square\n")
           # return False
        
        # Ensuring the piece belongs to the current player's turn
        if (turn == 'white' and piece[0] !='w') or (turn == 'black' and piece[0] !='b'):
            print ("Piece belongs to the opponent!\n")
            return False

        

        # Ensuring the target position is not occupied by the same player's piece
        if (target_piece != '.' and target_piece[0] == piece[0]):
            #print ("Cannot move piece to another position of your piece!")
            return False
        
        #Ensuring that the empty squares are always valid
        if target_piece =='.':
            return True

        
        # pieceType is either K,Q,B,N,p
        piece_Type = piece[1]


        #This whole section will determine that allowed moves of each chess pieces
        
        #Checking if the King is moving in only 1 Square Direction
        if (piece_Type == 'K'):
            return abs(start_row - end_row) <=1 & abs(start_col - end_col) <=1   #Takes the absolute value of the subtracted start and end position and checks if it's == 1
        
        #Checking if the Queen moves correctly
        elif (piece_Type =='Q'):
            # Checks if it's moving horizontally, vertically or diagnonally
            if start_row == end_row or start_col == end_col or abs(start_row - end_row) == abs(start_col - end_col): 
                return self.is_path_clear (game_state,move)  # Calling the helper function to check if the path is clear for the piece to move

        #Checking if the Bishop is moving correctly
        elif (piece_Type =='B'):
            # Checks if the bishop is moving diagonally
            if abs(start_row - end_row) == abs(start_col - end_col):
                return self.is_path_clear(game_state,move)  # Calling the helper function to check if the path is clear for the piece to move
            
        #Checking if the Knight is moving correctly
        elif (piece_Type =='N'):
            #Checks if the knight is moving in an L shape
            return (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)] # Checks if move 2 squares in one direction and 1 squre in perpendicular and vice versa
                
            
        # Checks if the pawn is moving correctly
        elif (piece_Type =='p'):
            if (piece[0]=='w'):  # Checks if pawn piece is white, then it'll move up
                direction = -1   # Negative as if it's going "down" a row index
            else:
                direction = 1 #Else if pawn piece is black, then it'll move down

            # Normal forward move
            # Checks if the pawn is only moving up and down the column with the direction given and checks if where it's moving is an empty space
            if end_col == start_col and end_row == start_row + direction and board[end_row][end_col] == '.':
                return True

            #Capturing a piece diagonally
            #Checks if the change in column in only 1, if the change in diection is 1, if the target_piece is not empty and  if the piece is not capturing it's own color
            if abs(end_col - start_col) == 1 and end_row == start_row + direction and target_piece != '.' and target_piece[0] != piece[0]:
                return True

            # Pawn reaching the end becoming Queen
            # If the white piece reaches the last row(0) or if the black reaches it's last row (4)
            if (piece[0] =='w' and end_row ==0) or (piece[0] =='b' and end_row ==4):
                return True

        return False

    
    """
    Helper function that checks if the path is clear for sliding pieces (specifically for Queens and Bishops)
    
    Args: 
        - game_state:   dictionary | Dictionary representing the current game state
        - move          tuple | the move which we check the validity of ((start_row, start_col),(end_row, end_col))
    Returns:
        - boolean representing if the path is clear

    """
    def is_path_clear(self, game_state, move):    

        #Getting the position of the start piece and it's desire end position
        start = move[0]  # Position of start piece. Ex: Let's take one 'wp', start = (3,1)
        end = move[1]  # Desired end position. Ex: (2,1)
        start_row, start_col = start # start position is unpacked into start_row (3), start_col(1)
        end_row, end_col = end # Ending position is unpacked into end_row (2), end_col (1)
        board = game_state["board"]  # Extracts the game board from game_state dictionary, allows modifying board easily
        
        # Determine row step
        if start_row == end_row:
            row_step =0            # Staying in the same row
        elif end_row > start_row:
            row_step = 1           # Moving down the board
        else:
            row_step= -1           # Moving up the board

        #Determine column step
        if start_col == end_col:
            col_step = 0            # Staying in same column
        elif end_col > start_col:
            col_step = 1            # Moving right
        else:
            col_step = -1           # Moving left

        #Assigning the row,col
        row, col = start_row + row_step, start_col + col_step  # This is initial movement of the piece one step at a time 


        while (row, col) != (end_row, end_col):  # Moving one step at a time along the path and if it reaches end_row, end_col, the path is clear
            if board[row][col] != '.':           # If it encounters any square that is not empty ('.') then the path is blocked 
                return False                     # Blocked Path
            row += row_step                      # Incrementing a row_step
            col += col_step                      # Incrementing col_step

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
        
        moves = []                     #Initializing list of valid moves
        board = game_state["board"]    # Extracting game board
        turn = game_state["turn"]      # Extracting the current player turn

        for r in range (5):  #Loops through all the rows
            for c in range (5):   #Loops through all columns
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
    
    """
    Generates all possible moves for a given piece before validation.

    Args:
        - game_state: dictionary | The current game state
        - piece: str | The chess piece (e.g., 'wK', 'bQ', 'wp')
        - position: tuple | The current position of the piece (row, col)

    Returns:
        - moves: list | A list of tuples representing all possible moves [(start, end), (start, end)]
    """
    def get_piece_moves(self, game_state, piece, position):
        
        moves = []                        #Initializing the list of possible moves that the player can do
        start_row, start_col = position   #Starting position of the piece
        board = game_state["board"]       #Getting the current board state
        piece_type = piece[1]             #Extracts the piece type whether it's K, Q, B, N, p

        if piece_type == 'K':                # King moves 1 square in any direction
            for dr in [-1, 0, 1]:            
                for dc in [-1, 0, 1]:     
                    if dr == 0 and dc == 0:   #Continue since it's just in place
                        continue
                    end = (start_row + dr, start_col + dc)   #Computes new position
                    if 0 <= end[0] < 5 and 0 <= end[1] < 5:  #Making sure that the move is within the board
                        moves.append((position, end))

        elif piece_type == 'Q':  # Checks if Queen could move in any direction
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
            for dr, dc in directions:
                for step in range(1, 5):  # Could move up to 4 squares 
                    end = (start_row + dr * step, start_col + dc * step)
                    if 0 <= end[0] < 5 and 0 <= end[1] < 5:
                        moves.append((position, end))
                        if board[end[0]][end[1]] != '.':  # Stop at first obstacle
                            break

        elif piece_type == 'B':  # Bishop moves diagonally
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                for step in range(1, 5):  #Move up to 4 squares diagonally
                    end = (start_row + dr * step, start_col + dc * step)
                    if 0 <= end[0] < 5 and 0 <= end[1] < 5:
                        moves.append((position, end))
                        if board[end[0]][end[1]] != '.':  # Stop at first obstacle
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





    """
    Modify to board to make a move

    Args: 
        - game_state:   dictionary | Dictionary representing the current game state
        - move          tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    Returns:
        - game_state:   dictionary | Dictionary representing the modified game state
    """
    def make_move(self, game_state, move):
        start = move[0]  # Position of start piece. Ex: Let's take one 'wp', start = (3,1)
        end = move[1]  # Desired end position. Ex: (2,1)
        start_row, start_col = start # start position is unpacked into start_row (3), start_col(1)
        end_row, end_col = end # Ending position is unpacked into end_row (2), end_col (1)
        piece = game_state["board"][start_row][start_col]  # Finds the piece at the starting position on the board, in this case, it's 'wp'
        target_piece = game_state["board"][end_row][end_col] # Is the end piece
        
        game_state["board"][start_row][start_col] = '.'  #clearing the starting posiition after moving the piece
        game_state["board"][end_row][end_col] = piece  #Places the piece at the new position   #game_state["board"][2][1] = "wp"  # White Pawn moves to (2,1)
        
        # Checking if the move captures the opponent's King and the player wins
        if target_piece != '.' and len(target_piece)> 1 and target_piece[1] =='K':
            print (f"{game_state['turn'].capitalize()} is the winner! The opponent's King was captured. Congradulations!")
            exit(0) # Exits when the player has won the game

        # Promoting pawn to Queen
        if piece [1] == 'p':
            if (piece[0] =='w' and end_row ==0) or (piece[0] =='b' and end_row ==4):    # If the piece reaches the end
                print(f"Pawn promoted to Queen at {chr(end_col + ord('A'))}{5- end_row}") # Print the promote pawn
                game_state["board"][end_col]  = piece[0] +'Q'

        #Checking if a piece was captured
        current_piece_count = self.count_pieces()
        if current_piece_count < self.previous_piece_count:  # A piece was captured
            self.moves_since_capture = 0  # Reset draw counter
            self.previous_piece_count = current_piece_count  # Update piece count
        else:
            self.moves_since_capture += 1  # Increase draw counter


        # Updates the turn of the player
        if game_state["turn"] == "white":
            game_state["turn"] ="black"
        else:
            game_state["turn"] = "white"
        
        return game_state
    
    """
    Counts the number of pieces in the board

    Returns:
        piece_count: The number of pieces in the board

    """
    #Counting the number of pieces in the board
    def count_pieces(self):
        
        board = self.current_game_state["board"]
        piece_count = 0
        for row in board:
            for piece in row:
                if piece != '.':
                    piece_count +=1

        return piece_count



    """
    Parse the input string and modify it into board coordinates

    Args:
        - move: string representing a move "B2 B3"
    Returns:
        - (start, end)  tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    """
    def parse_input(self, move):
        try:
            start, end = move.split()  # "B2 B3" → start ="B2" and end ="B3"
            start = (5-int(start[1]), ord(start[0].upper()) - ord('A'))   # start = (start_row, start_col)
            
            #start[1] is the row
            #start[0] is the column
            # Thus, "B2" becomes start = (5-2,  ord('B') - ord('A')) = (3,1) (row=3, column = 1)
            
            
            end = (5-int(end[1]), ord(end[0].upper()) - ord('A'))
            
            #end[1] is the row
            #end[0] is the column
            # Thus, "B3" becomes start = (5-3,  ord('B') - ord('A')) = (2,1) (row=2, column = 1)

            return (start, end)
            #Example of final input: ((3,1), (2,1))
        except:
            return None

    
    def change_to_chess_notation(self, move):
        start, end = move
        start_row, start_col = start
        end_row, end_col = end

        start_position = f"{chr(start_col + ord('A'))}{5 - start_row}"
        end_position = f"{chr(end_col + ord('A'))}{5 - end_row}"
    
        return f"{start_position} {end_position}"
    
    
    """
    Game loop

    Args:
        - None
    Returns:
        - None
    """
    def play(self):   # Main game loop, runs until user exits
        
        # Informs players how to enter moves
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.") 
        
        # Runs indefintely until player exits or wins
        while True:  
            
            # Calling the display board and prints current board
            self.display_board(self.current_game_state)   
            
            moves = self.valid_moves(self.current_game_state)  # Storing all the possible valid moves in moves 
            
            # Print moves since last capture for debugging
            print(f"Moves since last capture: {self.moves_since_capture}/20")

            
            # Printing all the moves of the current player in numerical board coordinates
            # print(f"Valid Moves for {self.current_game_state['turn'].capitalize()}: {moves}")

            #Converting all moves to chess notation
            converted_moves = [self.change_to_chess_notation(move) for move in moves]
            print (f"Valid Moves for {self.current_game_state['turn'].capitalize()}: {converted_moves}")

            # Checking if the player has no valid moves (game over condition)
            if not moves:
                print(f"No valid moves left for {self.current_game_state['turn']}. Game over!")
                exit(0)
            
             # Check for draw condition
            if self.moves_since_capture >= 20:  # 10 turns (20 moves)
                print("Game Drawn! No captures in 10 turns.")
                break
            
            #Asks for player input, then stores whose turn it is and makes sure "white" or "black" starts with an uppercase letter in the prompt # Example: White to move: B2 B3
            move = input(f"{self.current_game_state['turn'].capitalize()} to move: ") 
            
            # If the player types "exit", the game prints "Game exited"
            if move.lower() == 'exit':
                print("Game exited.")
                exit(1)
            
            
            move = self.parse_input(move) # Calls the method to: # "B2 B3" → ["B2", "B3"]
            if not move or not self.is_valid_move(self.current_game_state, move): # Checks if the move follow game rules
                print("Invalid move. Try again.")
                continue

            self.make_move(self.current_game_state, move) #Updating the board with the new move

#___________________________________________________________________





if __name__ == "__main__":   # Running the game
    game = MiniChess()
    game.play()
