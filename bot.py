"""тупа игровой бот"""
import logging

from vkwave.bots import SimpleLongPollBot

from config import TOKEN, GROUP_ID
from middlewares import UserMiddleware
from blueprints import (
    menu_router,
    profile_router,
    games_router,
    coin_flip_router,
    bonus_router,
)

logging.basicConfig(level="DEBUG")

bot = SimpleLongPollBot(TOKEN, group_id=GROUP_ID)

bot.middleware_manager.add_middleware(UserMiddleware())


bot.dispatcher.add_router(profile_router)
bot.dispatcher.add_router(games_router)
bot.dispatcher.add_router(coin_flip_router)
bot.dispatcher.add_router(bonus_router)

# регаем последним чтобы сначала проверялись все остальные команды
bot.dispatcher.add_router(menu_router)

bot.run_forever()
