import time
import datetime

from vkwave.bots import (
    DefaultRouter,
    simple_bot_message_handler,
    PayloadFilter,
    SimpleBotEvent,
)

from db.models.user import User

bonus_router = DefaultRouter()


@simple_bot_message_handler(bonus_router, PayloadFilter({"command": "bonus"}))
async def bonus(event: SimpleBotEvent):
    user: User = event["current_user"]
    if time.time() - user.last_bonus_time <= 86400:
        return await event.answer(
            f"Бонус доступен раз в день, следующий будет доступен -"
            f" {datetime.datetime.fromtimestamp(86400 + user.last_bonus_time)}"
        )
    user.last_bonus_time = time.time()
    user.balance += 1000
    await user.commit()
    return await event.answer("Получен бонус 1000!")
