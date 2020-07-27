import time
import typing

import umongo
from umongo import fields

from ..db import Instance


instance: umongo.Instance = Instance.get_current().instance


@instance.register
class User(umongo.Document):
    uid = fields.IntegerField(required=True, unique=True)
    first_name = fields.StringField()
    balance = fields.IntegerField(default=0)
    last_bonus_time = fields.IntegerField(default=0)

    created_time = fields.IntegerField(default=time.time)

    class Meta:
        collection = instance.db.users

    @staticmethod
    async def create_user(
        uid: int, first_name: str
    ) -> typing.Union["User", typing.NoReturn]:
        user: User = User(uid=uid, first_name=first_name)
        await user.commit()
        return user

    @staticmethod
    async def get_user(uid: int) -> typing.Optional["User"]:
        user = await User.find_one({"uid": uid})
        return user
