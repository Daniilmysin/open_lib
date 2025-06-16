from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from models.book_act import find_book

rt = Router()


class FindBookState(StatesGroup):
    None

@rt.message(F.text)
async def find_book_handler(message:Message):
    book = await find_book(message.text)
    if book:
        exit()

    return