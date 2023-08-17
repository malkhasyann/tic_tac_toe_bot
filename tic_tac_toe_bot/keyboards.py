from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from callbacks import ReadyCallback, ExitCallback


def get_ready_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='OK',
        callback_data=ReadyCallback()
    )
    
    return builder.as_markup()


def get_exit_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='No',
        callback_data=ExitCallback()
    )
    builder.button(
        text='Yes',
        callback_data=ReadyCallback()
    )
    
    return builder.as_markup()