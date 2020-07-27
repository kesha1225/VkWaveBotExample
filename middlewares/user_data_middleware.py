import typing
from vkwave.bots import BaseMiddleware, BotEvent, MiddlewareResult

from db.models.user import User


class UserMiddleware(BaseMiddleware):
    async def pre_process_event(self, event: BotEvent) -> MiddlewareResult:
        user_id = event.object.object.message.from_id

        user: typing.Optional[User] = await User.get_user(user_id)

        if user is None:
            user_data = await event.api_ctx.users.get(user_ids=user_id)
            user = await User.create_user(
                uid=user_id, first_name=user_data.response[0].first_name
            )

        event["current_user"] = user
        return MiddlewareResult(True)
