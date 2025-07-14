from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.enums import ParseMode

from models import find_author
from models.book_act import find_book

rt = Router()


class FindBookState(StatesGroup):
    None

async def book_writer(book) ->str :
    author = await find_author(book.author)
    book_str = f'/book {book.id}\n<b>{book.name}</b> \n Автор: {author.name} '
    return book_str

@rt.message(F.text)
async def find_book_handler(message:Message):
    book = await find_book(message.text)
    if book:
        exit()

    return