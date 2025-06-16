from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message


rt = Router()


class FindBookState(StatesGroup):
    None

@rt.message(F.text)
async def find_book(message:Message):
    None