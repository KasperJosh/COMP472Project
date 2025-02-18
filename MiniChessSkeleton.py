import copy

class MiniChess:
    def __init__(self):
        self.current_game_state = self.init_board()

    def init_board(self):
        state = {
            "board": [
                ['bK', 'bQ', 'bB', 'bN', '.'],
                ['.', '.', 'bp', 'bp', '.'],
                ['.', '.', '.', '.', '.'],
                ['.', 'wp', 'wp', '.', '.'],
                ['.', 'wN', 'wB', 'wQ', 'wK']
            ],
            "turn": 'white',
            "turn_count": 0,
            "last_capture_turn": 0
        }
        return state

    def display_board(self, game_state):
        print("\n  A   B   C   D   E")
        print(" +---+---+---+---+---+")
        for i, row in enumerate(game_state["board"], start=1):
            print(f"{6 - i}| " + " | ".join(piece if piece != '.' else ' ' for piece in row) + " |")
            print(" +---+---+---+---+---+")
        print()

    def is_valid_move(self, game_state, move):
        start, end = move
        start_row, start_col = start
        end_row, end_col = end
        board = game_state["board"]
        piece = board[start_row][start_col]
        
        if piece == '.':
            return False  # No piece to move
        
        if (game_state['turn'] == 'white' and piece[0] != 'w') or (game_state['turn'] == 'black' and piece[0] != 'b'):
            return False  # Not the player's piece
        
        target_piece = board[end_row][end_col]
        if target_piece != '.' and target_piece[0] == piece[0]:
            return False  # Can't capture own piece
        
        return self.validate_piece_movement(piece, start, end, board)
    
    def validate_piece_movement(self, piece, start, end, board):
        start_row, start_col = start
        end_row, end_col = end
        
        if piece[1] == 'K':  # King
            return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1
        elif piece[1] == 'Q':  # Queen
            return self.is_valid_straight_or_diagonal(start, end, board)
        elif piece[1] == 'B':  # Bishop
            return self.is_valid_diagonal(start, end, board)
        elif piece[1] == 'N':  # Knight
            return (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)]
        elif piece[1] == 'p':  # Pawn
            direction = -1 if piece[0] == 'w' else 1
            if start_col == end_col and board[end_row][end_col] == '.':
                return end_row - start_row == direction
            if abs(start_col - end_col) == 1 and end_row - start_row == direction:
                return board[end_row][end_col] != '.'  # Capture condition
        return False
    
    def is_valid_straight_or_diagonal(self, start, end, board):
        return self.is_valid_straight(start, end, board) or self.is_valid_diagonal(start, end, board)

    def is_valid_straight(self, start, end, board):
        start_row, start_col = start
        end_row, end_col = end
        
        if start_row == end_row:
            step = 1 if end_col > start_col else -1
            for c in range(start_col + step, end_col, step):
                if board[start_row][c] != '.':
                    return False
            return True
        
        if start_col == end_col:
            step = 1 if end_row > start_row else -1
            for r in range(start_row + step, end_row, step):
                if board[r][start_col] != '.':
                    return False
            return True
        
        return False
    
    def is_valid_diagonal(self, start, end, board):
        start_row, start_col = start
        end_row, end_col = end
        
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False
        
        step_r = 1 if end_row > start_row else -1
        step_c = 1 if end_col > start_col else -1
        r, c = start_row + step_r, start_col + step_c
        
        while r != end_row and c != end_col:
            if board[r][c] != '.':
                return False
            r += step_r
            c += step_c
        
        return True

    def make_move(self, game_state, move):
        start, end = move
        start_row, start_col = start
        end_row, end_col = end
        piece = game_state["board"][start_row][start_col]
        game_state["board"][start_row][start_col] = '.'
        game_state["board"][end_row][end_col] = piece
        game_state["turn"] = "black" if game_state["turn"] == "white" else "white"
        game_state["turn_count"] += 1
        
        if piece[1] == 'p' and (end_row == 0 or end_row == 4):
            game_state["board"][end_row][end_col] = piece[0] + 'Q'  # Pawn promotion
        
        if game_state["board"][end_row][end_col][1] == 'K':
            print(f"{game_state['turn'].capitalize()} wins!")
            exit()

    def parse_input(self, move):
        try:
            start, end = move.split()
            start = (5 - int(start[1]), ord(start[0].upper()) - ord('A'))
            end = (5 - int(end[1]), ord(end[0].upper()) - ord('A'))
            return (start, end)
        except:
            return None

    def play(self):
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.")
        while True:
            self.display_board(self.current_game_state)
            move = input(f"{self.current_game_state['turn'].capitalize()} to move: ")
            if move.lower() == 'exit':
                print("Game exited.")
                break
            move = self.parse_input(move)
            if not move or not self.is_valid_move(self.current_game_state, move):
                print("Invalid move. Try again.")
                continue
            self.make_move(self.current_game_state, move)

if __name__ == "__main__":
    game = MiniChess()
    game.play()
