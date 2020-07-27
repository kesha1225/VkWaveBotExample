from vkwave.bots import (
    DefaultRouter,
    SimpleBotEvent,
    simple_bot_message_handler,
    PayloadFilter,
)

from utils.constants import GAMES_KB

games_router = DefaultRouter()


@simple_bot_message_handler(games_router, PayloadFilter({"command": "games"}))
async def games(event: SimpleBotEvent):
    return await event.answer(
        message=f"Выберите игру", keyboard=GAMES_KB.get_keyboard()
    )
