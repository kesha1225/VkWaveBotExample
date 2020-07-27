import datetime

from vkwave.bots import (
    DefaultRouter,
    SimpleBotEvent,
    simple_bot_message_handler,
    PayloadFilter,
)

from db.models.user import User

profile_router = DefaultRouter()


@simple_bot_message_handler(profile_router, PayloadFilter({"command": "profile"}))
async def profile(event: SimpleBotEvent):
    user: User = event["current_user"]
    return await event.answer(
        message=f"Ваш профиль:\n\n"
        f"id - {user.uid}\n"
        f"Имя - {user.first_name}\n"
        f"Баланс - {user.balance}\n"
        f"Дата регистрации - {datetime.datetime.fromtimestamp(user.created_time)}",
    )
