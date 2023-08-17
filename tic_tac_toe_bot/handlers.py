from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext

from game_state import GameState
from keyboards import get_ready_kb, get_exit_kb
from callbacks import MoveCellCallback, ReadyCallback, ExitCallback
from updates import update_board
from telegram_models.matches import Matches
from telegram_models.gamer import Gamer
from telegram_models.pair_session import PairSession


cell_mask = {0: '▫️', 1: '❌', 2: '⚫️'}


router = Router()


@router.message(F.text == 'test')
async def test_handler(
    message: Message,
    matches: Matches
):
    data = matches.data
    msg_text = 'Matches:\n' + '\n'.join(f'{pair[0]} v {pair[1]}' for pair in data)
    gm_text = 'Gamers:\n' + '\n'.join(f'{gamer.user.id}: {gamer.player.name}' for gamer in matches.gamers)
    session_text = 'Open Sessions:\n' + '\n'.join(f'{session.code}' for session in matches.sessions)

    await message.answer(msg_text)
    await message.answer(gm_text)
    await message.answer(session_text)


@router.message(Command('start'))
async def cmd_start(
    message: Message,
    state: FSMContext
):
    await state.set_state(GameState.connection_state)
    
    await message.answer(
        text=f'Welcome, {message.from_user.full_name}'
    )
  

@router.message(
    Command('new_game'),
    GameState.connection_state
)
async def cmd_new_game(
    message: Message,
    matches: Matches,
    state: FSMContext
):
    gamer1 = Gamer(message.from_user, order=1)
    session = PairSession(gamer1)
    matches.add_gamer(gamer1)
    matches.add_session(session)
    
    await state.set_state(GameState.ready_state)
    
    await message.answer(
        text=f'You created a new game sessions.\n\n'
            'Connection code:'
    )    
    await message.answer(
        text=f'{session.code}'
    )
    

@router.message(
    Command('connect'),
    GameState.connection_state
)
async def cmd_connect(
    message: Message,
    state: FSMContext,
    bot: Bot,
    matches: Matches,
    command: CommandObject
):
    code = command.args.strip()
    
    session = matches.get_session_by_code(code)
    
    if not session:
        await message.answer(
            text=f'The code is invalid.Try Again.'
        )
        return
    
    gamer2 = Gamer(message.from_user, order=3 - session.gamer1.player.order)
    session.to_pair(gamer2)
    matches.add_match(session)
    matches.add_gamer(gamer2)
    
    user1 = session.gamer1.user
    
    await state.set_state(GameState.ready_state)
    
    await message.answer(
        text=f'You and {user1.full_name} are connected.\n\n'
            f'Press OK to start the game.',
        reply_markup=get_ready_kb()
    )
    
    await bot.send_message(
        chat_id=user1.id,
        text=f'You and {message.from_user.full_name} are connected.\n\n'
            f'Press OK to start the game.',
        reply_markup=get_ready_kb()
    )
    
    
@router.callback_query(
    ReadyCallback.filter(),
    GameState.ready_state
)
async def ready_cb_handler(
    callback: CallbackQuery,
    bot: Bot,
    state: FSMContext,
    matches: Matches
):
    current_user = callback.from_user
    current_gamer = matches.get_gamer_by_id(current_user.id)
    
    # opponent_gamer = matches.get_gamer_opponent_by_id(current_user.id)
    # opponent_user = opponent_gamer.user
    
    session = matches.get_game_session_by_gamer(current_gamer)
    
    symbol = cell_mask[session.to_move.order]
    
    game_message = await bot.send_message(
        chat_id=current_user.id,
        text=f"{symbol}       {session.to_move.name}'s turn       {symbol}",
        reply_markup=current_gamer.get_board()
    )
    
    current_gamer.message = game_message
    
    await state.set_state(GameState.gameplay_state)
    
    await callback.answer()
    
    
@router.callback_query(
    GameState.gameplay_state,
    MoveCellCallback.filter()
)
async def move_handler(
    callback: CallbackQuery,
    callback_data: MoveCellCallback,
    state: GameState,
    matches: Matches,
    bot: Bot
):
    current_gamer = matches.get_gamer_by_id(callback.from_user.id)
    game_session = matches.get_game_session_by_gamer(current_gamer)
    opponent = matches.get_gamer_opponent_by_id(current_gamer.user.id)
    
    if (current_gamer.player is not game_session.to_move) or game_session.winner:
        await callback.answer()
        return
    
    move_coords = tuple(
        int(i) for i in
        callback_data.value.split()
    )
    
    game_session.move(*move_coords)
    
    await update_board(gamer=current_gamer, game_session=game_session)
    await update_board(gamer=opponent, game_session=game_session)
    
    if game_session.check_game_over():
        if game_session.winner:
            msg_text = f'Wow!! {game_session.winner.name} wins the game 💪👑'
        else:
            msg_text = "It's draw 💫🤝💫"
            
        await bot.send_message(
            chat_id=current_gamer.user.id,
            text=msg_text
        )
        
        await bot.send_message(
            chat_id=opponent.user.id,
            text=msg_text
        )
        
        await bot.send_message(
            chat_id=current_gamer.user.id,
            text=f'Would you like to play together once more?🎮',
            reply_markup=get_exit_kb()
        )
        
        await bot.send_message(
            chat_id=opponent.user.id,
            text=f'Would you like to play together once more?🎮',
            reply_markup=get_exit_kb()
        )
    
    await callback.answer()
    
    
@router.callback_query(
    GameState.gameplay_state,
    ExitCallback.filter()
)
async def exit_cb_handler(
    callback: CallbackQuery,
    state: FSMContext, 
    matches: Matches,
):
    await state.set_state(GameState.connection_state)
    
    user1 = callback.from_user
    gamer1 = matches.get_gamer_by_id(user1.id)
    session = matches.get_session_by_id(user1.id)
    
    matches.delete_match_by_gamer_id(user1.id)

    matches.delete_gamer(gamer1)
    
    await callback.answer()
    
    
@router.callback_query(
    GameState.gameplay_state,
    ReadyCallback.filter()
)
async def again_ready_handler(
    callback: CallbackQuery,
    matches: Matches,
    state: FSMContext,
    bot: Bot
):
    await state.set_state(GameState.ready_state)
    
    current_user = callback.from_user
    
    opp_gamer = matches.get_gamer_opponent_by_id(current_user.id)
    
    if not opp_gamer:
        await state.set_state(GameState.connection_state)
        await bot.send_message(
            chat_id=current_user.id,
            text=f'Sorry, but your opponent left the session.👀'
        )
        await callback.answer()
        return
    
    current_gamer = matches.get_gamer_by_id(current_user.id)
    new_order = 1 if current_gamer.player.order == 2 else 2
    new_gamer = Gamer(current_user, order=new_order)
    
    waiting_session = matches.get_waiting_session_by_id(opp_gamer.user.id)
    if not waiting_session:
        new_session = PairSession(new_gamer)
        matches.add_gamer(new_gamer)
        matches.add_session(new_session)
        matches.delete_gamer(current_gamer)
        
        await callback.answer()
        return
        
    waiting_session.to_pair(new_gamer)
    matches.add_match(waiting_session)
    matches.add_gamer(new_gamer)

    matches.delete_gamer(current_gamer)

    await bot.send_message(
        chat_id=new_gamer.user.id,
        text=f'You and {opp_gamer.user.full_name} are connected.\n\n'
            f'Press OK to start the game.',
        reply_markup=get_ready_kb()
    )

    await bot.send_message(
        chat_id=opp_gamer.user.id,
        text=f'You and {new_gamer.user.full_name} are connected.\n\n'
            f'Press OK to start the game.',
        reply_markup=get_ready_kb()
    )
        
    await callback.answer()