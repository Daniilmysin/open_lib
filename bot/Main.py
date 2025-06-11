import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from Handlers.debug import info
from Handlers.user import add_book, add_author, other
from models import db_act

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


# Запуск бота
async def main():
    try:
        load_dotenv()
        Bot_token = str(os.getenv('bot'))
        if Bot_token is None:
            exit(print('Bot token does not exist'))
    except Exception:
        exit(print(f".env file read error"))

    bot = Bot(token=Bot_token)

    try:
        await db_act.make_bd()
    except Exception as error:
        print(f"Ошибка создания базы данных: {error}")
        exit()
    # Диспетчер
    dp = Dispatcher()
    dp.include_routers(add_book.rt, other.rt, info.rt, add_author.rt)
    await dp.start_polling(bot)  # запускаем


if __name__ == "__main__":
    asyncio.run(main())
