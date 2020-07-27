import json
import random

from vkwave.bots import (
    DefaultRouter,
    SimpleBotEvent,
    simple_bot_message_handler,
    PayloadFilter,
    FiniteStateMachine,
    State,
    ForWhat,
    StateFilter,
    CommandsFilter,
    Keyboard,
)

from db.models.user import User
from utils.constants import MENU_KB

coin_flip_router = DefaultRouter()

fsm = FiniteStateMachine()


class CoinState:
    bet = State("bet")
    coin = State("coin")


@simple_bot_message_handler(coin_flip_router, CommandsFilter("exit"))
async def games(event: SimpleBotEvent):
    if await fsm.get_data(event, for_what=ForWhat.FOR_USER) is not None:
        await fsm.finish(event=event, for_what=ForWhat.FOR_USER)
    return await event.answer(
        message=f"Выберите дальнейшее действие, {event['current_user'].first_name}",
        keyboard=MENU_KB.get_keyboard(),
    )


@simple_bot_message_handler(coin_flip_router, PayloadFilter({"command": "coin_flip"}))
async def start_coin_flip(event: SimpleBotEvent):
    await fsm.set_state(event=event, state=CoinState.bet, for_what=ForWhat.FOR_USER)
    return await event.answer(
        message=f"Введите ставку, если передумали пишите /exit ",
        keyboard=Keyboard.get_empty_keyboard(),
    )


@simple_bot_message_handler(
    coin_flip_router,
    StateFilter(fsm=fsm, state=CoinState.bet, for_what=ForWhat.FOR_USER),
)
async def bet_router(event: SimpleBotEvent):
    user: User = event["current_user"]
    bet = event.object.object.message.text
    if not bet.isdigit() or int(bet) <= 0:
        return await event.answer(message=f"Нужно число большее нуля.")
    if int(bet) > user.balance:
        return await event.answer(message=f"у вас стока нет")
    kb = Keyboard()
    kb.add_text_button("Орел", payload={"coin": "heads"})
    kb.add_text_button("Решка", payload={"coin": "tails"})
    await fsm.set_state(
        event=event,
        state=CoinState.coin,
        for_what=ForWhat.FOR_USER,
        extra_state_data={"bet": bet},
    )
    return await event.answer(
        message=f"Ставка {bet} успешно сделана. Как упадет монетка?",
        keyboard=kb.get_keyboard(),
    )


@simple_bot_message_handler(
    coin_flip_router,
    StateFilter(fsm=fsm, state=CoinState.coin, for_what=ForWhat.FOR_USER),
)
async def final_coin_flip(event: SimpleBotEvent):
    user: User = event["current_user"]
    coin_type = json.loads(event.object.object.message.payload)["coin"]
    data = await fsm.get_data(event=event, for_what=ForWhat.FOR_USER)
    bet = data["bet"]
    random_coin = random.choice(["heads", "tails"])
    await fsm.finish(event=event, for_what=ForWhat.FOR_USER)
    if coin_type == random_coin:
        win_value = int(bet) * 2
        user.balance += win_value
        await user.commit()
        return await event.answer(
            message=f"Вы угадали! Выигрыш - {win_value}",
            keyboard=MENU_KB.get_keyboard(),
        )
    user.balance -= int(bet)
    await user.commit()
    return await event.answer(
        message=f"Вы не угадали((", keyboard=MENU_KB.get_keyboard()
    )
