# Mini Chess COMP472 Project
MiniChess Project for COMP472 Artificial Intelligence 


### Description

Mini Chess is a 2-player game, inspired by the game of chess, played with the white pieces and the black pieces on a 5×5 board. Each player (white/black pieces) has 6 pieces on the board. 
These pieces are: 
    King (K): The King moves 1 square in any direction. The goal of the game is to capture the opponent’s king 
    Queen (Q): The Queen moves any number of squares in any direction. 
    Bishop (B): The Bishop moves diagonally. K
    night (N): The Knight moves in an L-shape (2 squares in one direction and 1 in a perpendicular direction). 
    pawns (p): Each player has 2 pawns. Pawns move 1 square forward, capturing diagonally. Pawns promote to a Queen upon reaching the 5th row opposite their side.


### Features:
    - Contains a playable 5x5 board
    - Supports the standard chess pieces above: King, Queen, Bishop, Knight and Pawns
    - Implements basic chess rules, including pawn promotion and win/draw condition
    - Logs all moves and board states to a trace file

### Installation

1. Clone the repository: 
    git clone https://github.com/KasperJosh/COMP472Project.git
2. Navigate to to the project directory:
    cd COMP472Project
3. Run the game:
    python MiniChessOfficial.py

### Usage

- Start the game by running 'python MiniChessOfficial.py'
- Enter moves in the format `B2 B3` (start position followed by end position).
- Type `exit` to quit the game.

### Rules
- White always moves first.
- Pawns promote to Queens when reaching the opposite end of the board.
- The game ends when a player captures the opponent's King or if no captures occur in 10 turns (draw).

### Brief Explanation of Methods
    
    __init__(self) :  
        -   Initializes the game
    init_board(self): 
        -   Creates the initial game board
    display_board(self, game_state): 
        -   Displays the current state of the board
    is_valid_move (self, game_stae,move): 
        -   Checks if a move is valid for the current game state
        -   Checks Moves based on the board boundaries, piece ownership and the movement rules for each piece type
    is_path_clear (self, game_state, move): 
        -   Checks if the path between two positions is clear and that there's no pieces blocking
    valid_moves (self, game_state): 
        -   Generates all valid moves for the current player
        -   Iterates through all of the pieces and checks all of their possible moves
    print_possible_moves(self, game_state, move): 
        -   Executes a move and updates the game state
        -   Moves the pieces, handles pawn promotion to Queen, logs move to trace file, updates the draw counter
    log_action(self, game_state, move): 
        -   Logs the move and board stae to the trace file
    count_pieces (self): 
        -   Counts the number of pieces remaining on the board
    parse_input(self,move): 
        -   Parses user input into board coordinates
    play(self): 
        -   Main Game Loop

### Credits
- Developed by [Joshua Visario](https://github.com/KasperJosh).