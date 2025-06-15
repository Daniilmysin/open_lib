from aiogram.filters import BaseFilter
from aiogram.types import Message
from models import find_user


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message):
        self.user = await find_user(message.from_user.id)
        return self.user.admin