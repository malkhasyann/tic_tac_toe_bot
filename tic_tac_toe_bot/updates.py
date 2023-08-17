from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest

from telegram_models.gamer import Gamer, cell_mask
from models.session import GameSession


async def update_board(
    gamer: Gamer,
    game_session: GameSession
):
    symbol = cell_mask[game_session.to_move.order]
    
    with suppress(TelegramBadRequest):
        await gamer.message.edit_reply_markup(
            reply_markup=gamer.get_board()
        )    
    
    with suppress(TelegramBadRequest):
        await gamer.message.edit_text(
            text=f"{symbol}       {game_session.to_move.name}'s turn       {symbol}",
            reply_markup=gamer.get_board()
        )