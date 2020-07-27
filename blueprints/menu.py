from vkwave.bots import DefaultRouter, SimpleBotEvent, simple_bot_message_handler

from utils.constants import MENU_KB

menu_router = DefaultRouter()


@simple_bot_message_handler(menu_router,)
async def menu(event: SimpleBotEvent):
    return await event.answer(
        message=f"Выберите дальнейшее действие, {event['current_user'].first_name}",
        keyboard=MENU_KB.get_keyboard(),
    )
