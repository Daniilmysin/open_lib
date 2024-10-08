from aiogram import types


def get_start_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="Добавить книгу", callback_data="add_book"),
            types.InlineKeyboardButton(text="Добавить автора", callback_data="add_author")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_keyboard_save_book():
    buttons = [
        [
            types.InlineKeyboardButton(text="Cохранить", callback_data="save_book"),
            types.InlineKeyboardButton(text="Изменить", callback_data="change_book"),
            types.InlineKeyboardButton(text="Заново", callback_data="add_book")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_keyboard(button, command):
    buttons = [
        [
            types.InlineKeyboardButton(text=button, callback_data=command),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
