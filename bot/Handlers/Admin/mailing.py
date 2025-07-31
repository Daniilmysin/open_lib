import asyncio

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from bot.filter import AdminFilter
from models import all_user

rt = Router()
rt.message.filter(AdminFilter())
class StateMailing(StatesGroup):
    getmail = State()


@rt.message(Command('mailing'))
async def start_mailing(message:Message, state: FSMContext):
    await message.answer("Отправьте сообщение для рассылки или нажмите /stop для отмены")
    await state.set_state(StateMailing.getmail)

@rt.message(Command(''))
async def stop_mailing(message:Message, state: FSMContext):
    await message.answer("Отмена")
    await state.clear()

@rt.message(F.text, StateFilter(StateMailing.getmail))
async def mailing(message:Message, state: FSMContext):
    async def send(chat):
        async with asyncio.Semaphore(10):
            await message.bot.send_message(chat_id=chat, text=message.text)
    users = await all_user()
    tasks = [send(chat) for chat in users]
    await asyncio.gather(*tasks)
