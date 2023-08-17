from aiogram.fsm.state import StatesGroup, State


class GameState(StatesGroup):
    connection_state = State()
    ready_state = State()
    gameplay_state = State()