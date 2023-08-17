class Board:
    def __init__(self):
        self.data: list[list] = [
            [0 for _ in range(3)] for _ in range(3)
        ]
        self.free_cells: list[tuple] | None = None
        self.update_free_cells()
    
    def set_at(self, i: int, j: int, value: int) -> bool:
        '''
        Returns whether the value is set properly.
        '''
        if (i, j) not in self.free_cells:
            return False
        
        self.data[i][j] = value
        self.update_free_cells()
        return True
        
    def update_free_cells(self) -> None:
        self.free_cells = [
            (i, j) 
            for i in range(3) for j in range(3) 
            if self.data[i][j] == 0
        ]
        
    