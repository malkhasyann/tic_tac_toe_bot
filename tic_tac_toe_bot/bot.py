import logging
import asyncio

from aiogram import Bot, Dispatcher

import handlers
from telegram_models.matches import Matches
from config_reader import config


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    
    # dp.include ...
    dp.include_router(handlers.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    # TODO: remember to add here matches object
    await dp.start_polling(bot, matches = Matches())
    
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())