import os
import secrets

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from bot.keyboard import get_keyboard_save_book, get_keyboard
from models import BookAdd
from models import RedisManager
from bot.scripts import transliterate

rt = Router()
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
allowed_formats = ['.pdf', '.epub', '.fb2', '.txt']

class AddingBook(StatesGroup):
    get_adder_author = State()
    get_adder_name = State()
    get_adder_des = State()
    get_adder_files = State()
    end = State()


@rt.callback_query(F.data == "add_book")
async def ins_book(callback: types.CallbackQuery, state: FSMContext):
    """Начинает процесс добавления книги"""
    await callback.message.answer("Введите ID Автора."
                                  "Если автора нет в базе данных, то добавьте его",
                                  reply_markup=get_keyboard('Добавить автора', 'add_author'))
    await state.set_state(AddingBook.get_adder_author)


@rt.message(F.text, StateFilter(AddingBook.get_adder_author))
async def ins_book_author(message: Message, state: FSMContext):
    """Принимает айди автора"""
    mes = int(message.text)
    status = await BookAdd().author_id(mes, message.from_user.id)
    if status is True:
        await message.answer("Добавлено. Введите название книги:")
        await state.set_state(AddingBook.get_adder_name)
    elif status is None:
        await message.answer("Автор не найден, повторите или добавьте автора с помощью /add_author")
        await state.set_state(AddingBook.get_adder_author)
    else:
        await message.answer("Что-то сломалось, повторите")
        await state.set_state(AddingBook.get_adder_author)


@rt.message(F.text, StateFilter(AddingBook.get_adder_name))
async def ins_book_name(message: Message, state: FSMContext):
    """Принимает название книги"""
    mes = str(message.text)
    status = await BookAdd().add_data(id_user=message.from_user.id, add_data=mes, key='name')
    """Если всё нормально то всё True"""
    if status is True:
        await message.answer("Добавлено. Напишите описание книги")
        await state.set_state(AddingBook.get_adder_des)
    else:
        await message.answer("Что-то сломалось, повторите")
        await state.set_state(AddingBook.get_adder_name)


@rt.message(F.text, StateFilter(AddingBook.get_adder_des))
async def ins_book_name(message: Message, state: FSMContext):
    """Принимает описание"""
    mes = str(message.text)
    print(mes)
    status = await BookAdd().add_data(id_user=message.from_user.id, add_data=mes, key='description')
    """Если всё нормально то всё True"""
    if status is True:
        await message.answer("Добавлено. Отправьте файл книги")
        await state.set_state(AddingBook.get_adder_files)
    else:
        await message.answer("Что-то сломалось, повторите")
        await state.set_state(AddingBook.get_adder_name)


@rt.message(F.document, AddingBook.get_adder_files)
async def ins_book_files(message: Message, state: FSMContext):
    """принимает файл с книгой"""

    book = await RedisManager().get_data(message.from_user.id)  # получаем книгу

    save_folder = os.path.join(folder, 'books')
    document = message.document          # получаем документ
    file_info = await message.bot.get_file(document.file_id)
    book_format = str(os.path.splitext(document.file_name)[1])
    formats = book.get('formats') or []

    if book_format not in allowed_formats:
        await message.reply("Файл не подходит, отправьте другой")
        await state.set_state(AddingBook.get_adder_files)
        return

    if book_format in formats:
        await message.answer('Этот формат уже есть, отправьте другой')
        await state.set_state(AddingBook.get_adder_files)
        return

    formats.append(book_format)

    if book.get('file'):
        name = book['file']
    else:
        name = str(await transliterate(book['name'])) + '_' + str(secrets.token_hex(16))  # создание имени файла с токеном

    new_file_name = name + book_format
    downloaded_file = await message.bot.download_file(file_info.file_path)  # скачиваем
    destination = os.path.join(save_folder, new_file_name)

    try:
        with open(destination, 'wb') as f:  # сохраняем
            f.write(downloaded_file.read())
    except Exception as Error:
        print(f'Ошибка открытия файла:{Error}')
        await message.reply("Ошибка открытия и сохранения файла, возможно файл побит")

    await BookAdd().add_data(message.from_user.id, formats, 'formats')
    await BookAdd().add_data(message.from_user.id, name, 'file')
    await message.reply("Файл сохранен")
    await state.set_state(AddingBook.end)


@rt.callback_query(F.data == 'save_book', AddingBook.end)
async def end(callback: types.CallbackQuery, state: FSMContext):
    """Запускает скрипт с загрузкой книги в базу данных"""
    status = await BookAdd().end(callback.from_user.id)
    if status is True:
        await callback.message.answer("Книга сохранена")
        await state.clear()
    else:
        await callback.message.answer("Что-то сломалось")
        await state.set_state(AddingBook.end)


@rt.callback_query(F.data =="add_file")
async def stop(callback: types.CallbackQuery , state: FSMContext):
    """Заканчивает создание книги"""
    await callback.message.answer("Отправьте файл")
    await state.set_state(AddingBook.get_adder_files)


@rt.callback_query(F.data =="stop")
async def stop(callback: types.CallbackQuery , state: FSMContext):
    """Заканчивает создание книги"""
    await callback.message.answer("Отмена...")
    await RedisManager().del_data(callback.from_user.id)
    await state.clear()
