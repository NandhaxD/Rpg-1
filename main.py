import asyncio
from bot import bot, session
from sqlalchemy import select
from classes import Persons


async def main():
    await asyncio.gather(bot.infinity_polling())


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        stmt = select(Persons)
        users = session.scalars(stmt)
        for user in users:
            user.CurHP = user.HP
            user.LocationID = 1
            session.commit()
