'''The class Gamer encapsulates the models.Player
and aiogram.types.User classes functionality.'''


from aiogram.types import User, Message, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models.player import Player
from callbacks import MoveCellCallback

cell_mask = {0: '▫️', 1: '❌', 2: '⚫️'}

class Gamer:
    def __init__(self, user: User, order: int):
        self.user: User = user
        self.player: Player = Player(name=self.user.full_name, order=order)
        self.message: Message = None
        
    def get_board(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        matrix = self.player.board.data
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                builder.button(
                    text=cell_mask[matrix[i][j]],
                    callback_data=MoveCellCallback(value=f'{i} {j}')
                )
                
        builder.adjust(3)
                
        return builder.as_markup()