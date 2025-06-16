import orjson
import os

from typing import List
import redis.asyncio as aioredis
from dotenv import load_dotenv
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped,mapped_column

load_dotenv()
user = str(os.getenv("user"))
passwd = str(os.getenv("passwd"))
host = str(os.getenv("host"))
engine = create_async_engine(f"postgresql+asyncpg://{user}:{passwd}@{host}/postgres", echo=True)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = 'book'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey('author.id'))  # ссылка на автора
    description: Mapped[str]
    creator: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))  # ссылка на того что добавил книгу
    check: Mapped[bool] = mapped_column(default=False)
    file: Mapped[str]


class Author(Base):
    __tablename__ = 'author'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    creator: Mapped[int] = mapped_column(ForeignKey("user.id"))
    description: Mapped[str]
    photo: Mapped[str]
    check: Mapped[bool] = mapped_column(default=False)
    books: Mapped[List[Book]] = relationship()


class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    books: Mapped[List[Book]] = relationship()
    authors : Mapped[List[Author]] = relationship()
    admin: Mapped[bool] = mapped_column(default=False)
    ban: Mapped[bool] = mapped_column(default=False)


# класс работы с redis
class RedisManager:
    def __init__(self):
        self.redis = aioredis.Redis()

    async def set_data(self, key, data) -> bool:
        async with self.redis as r:
            try:
                serialized_data = orjson.dumps(data)
                await r.set(key, serialized_data)
                await r.aclose()
                return True
            except Exception as e:
                # Обработка ошибки
                print(f"Error setting data: {e}")
                return False

    async def get_data(self, key):
        async with self.redis as r:
            try:
                data = await r.get(key)
            except Exception as e:
                # Обработка ошибки
                print(f"Error getting data: {e}")
                return None
            if data:
                return orjson.loads(data)
            return False

    async def del_data(self, key):
        async with self.redis as r:
            try:
                await r.delete(key)
                await r.aclose()
            except Exception as e:
                # Обработка ошибки
                print(f"Error deleting: {e}")
                return False


async def del_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def make_bd():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
