from models.board import Board


class Player:
    def __init__(
      self,
      name: str,
      order: int
    ):
        self.name = name
        self.order = order  # 1 - X, 2 - O
        self.board: Board | None = None
        
    def move(self, i: int, j: int) -> bool:
        '''
        Returns True if the move was done properly, False otherwise.
        '''
        return self.board.set_at(i, j, self.order)
    
    def set_board(self, board: Board) -> None:
        self.board = board