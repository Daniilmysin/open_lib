from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from bot.Handlers.Admin.filter import AdminFilter
from models import find_user

rt = Router()
rt.message.filter(AdminFilter())
class StateMailing(StatesGroup):
    getmail = State()


@rt.message(Command('mailing'))
async def start_mailing(message:Message, state: FSMContext):
    user = await find_user(message.from_user.id)
    if user.admin is False:
        return
    await message.answer("Отправьте сообщение для рассылки")
    await state.set_state(StateMailing.getmail)

@rt.message(F.text, StateFilter(StateMailing.getmail))
async def mailing():
    return