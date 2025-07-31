import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import RedisManager, engine, Author

async def find_author(id_author):
    async with AsyncSession(engine) as session:
        result_author = await session.execute(select(Author).filter_by(id=id_author))
        author = result_author.scalar_one_or_none()
        try:
            await session.flush()
        except Exception as error:
            logging.error(f'поиск автора ошибка:{error},юзер:{id_author}')
            return False
    return author

class AddAuthor(RedisManager):
    async def name(self, id_user, name) -> bool:
        data = {
            "name": name
        }
        return await self.set_data(id_user, data)

    async def add_data(self, id_user, add_data, key):
        data = await self.get_data(id_user)
        data[str(key)] = add_data
        return await self.set_data(id_user, data)

    async def end(self, id_user):
        async with AsyncSession(engine) as session:
            data = await self.get_data(id_user)
            prompt = Author(
                name=data['name'],
                description=data['description'],
                photo=data['photo'],
                creator=id_user
            )
            session.add(prompt)
            await session.flush()
            await self.del_data(id_user)
            return prompt.id


async def delete(id_book, id_user) -> bool:
    pass
