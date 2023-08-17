from models.board import Board
from models.player import Player


class GameSession:
    def __init__(
      self,
      player1: Player,
      player2: Player  
    ):
        self.player1: Player = player1
        self.player2: Player = player2
        
        self.board: Board = Board()
        
        self.player1.set_board(self.board)
        self.player2.set_board(self.board)
        
        self.to_move: Player = player1 if player1.order == 1 else player2
        self.winner: Player | None = None
        self.is_game_over: bool = False
        
    def check_game_over(self):
        rows = [row for row in self.board.data]
        columns = [
            [
                self.board.data[i][j] 
                for i in range(len(self.board.data))
            ]
            for j in range(len(self.board.data))
        ]
        main_diag = [
            self.board.data[i][i]
            for i in range(len(self.board.data)) 
        ]
        
        second_diag = [
            self.board.data[i][len(self.board.data) - 1 - i]
            for i in range(len(self.board.data)) 
        ]
        
        # checking rows
        if any(all(num == self.player1.order for num in row) for row in rows):
            self.winner = self.player1
            return True
        
        if any(all(num == self.player2.order for num in row) for row in rows):
            self.winner = self.player2
            return True
        
        # checking columns  
        if any(all(num == self.player1.order for num in col) for col in columns):
            self.winner = self.player1
            return True
        
        if any(all(num == self.player2.order for num in col) for col in columns):
            self.winner = self.player2
            return True
        
        # checking main diagonal
        if all(num == self.player1.order for num in main_diag):
            self.winner = self.player1
            return True
        
        if all(num == self.player2.order for num in main_diag):
            self.winner = self.player2
            return True    
        
        # checking secondary diagonal
        if all(num == self.player1.order for num in second_diag):
            self.winner = self.player1
            return True
        
        if all(num == self.player2.order for num in second_diag):
            self.winner = self.player2
            return True
        
        if not self.board.free_cells:
            return True
        
        return False
        
    def move(self, i: int, j: int) -> None:
        next_player = self.player1 if self.to_move is self.player2 else self.player2
        if self.to_move.move(i, j):
            self.to_move = next_player
        self.is_game_over = self.check_game_over()
