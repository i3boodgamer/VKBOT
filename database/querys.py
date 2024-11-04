import logging

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from .models import VKUser, VKUserPromocode, VKUserNumber, VKLastMessage


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


async def get_user_table(session: AsyncSession, user_id: int) -> int:
    try:
        stmt = await session.execute(
            select(VKUser.vk_id)
            .where(VKUser.vk_id == user_id)
        )
        
        return stmt.scalars().one_or_none()
    except Exception as e:
        log.error(f"Ошибка при запросе: {e}")


async def get_user_table_promocode(session: AsyncSession, user_id: int) -> int:
    try:
        stmt = await session.execute(
            select(VKUserPromocode.vk_id)
            .where(VKUserPromocode.vk_id == user_id)
        )
        return stmt.scalars().one_or_none()
    except Exception as e:
        log.error(f"Ошибка при запросе: {e}")


async def add_user_table_promocode(session: AsyncSession, user_id: int):
    try:
        user=VKUserPromocode(
            vk_id=user_id,
            promocode=True,
        )
        session.add(user)
        await session.commit()
    except Exception as e:
        log.info(f"Данные не коретны. Ошибка {e}")


async def del_user_table(session: AsyncSession, user_id):
    user_delete = await session.get(VKUser, user_id)

    if user_delete:
        await session.delete(user_delete)
        await session.commit()


async def add_user_table(session: AsyncSession, user_id, name: str):
    try:
        user = VKUser(
            vk_id=user_id,
            name=name,
        )
        session.add(user)
        await session.commit()
    except Exception as e:
        log.info(f"Данные не коретны. Ошибка {e}")


async def mute_bot(session: AsyncSession, user_id: int):
    try:
        user: VKUser = (await session.execute(
            select(VKUser)
            .filter(VKUser.vk_id == user_id)
            )).scalars().one_or_none()
        user.muth = True
        
        session.add(user)
        await session.commit()
    except Exception as e:
        log.error(f"Ошибка при коммите {e}")


async def unmute_bot(session: AsyncSession, user_id: int):
    try:
        user: VKUser = (await session.execute(
            select(VKUser)
            .filter(VKUser.vk_id == user_id)
            )).scalars().one_or_none()
        log.info(user)
        user.muth = False
        
        session.add(user)
        await session.commit()
    except Exception as e:
        log.error(f"Ошибка при коммите {e}")
    

async def add_number(session: AsyncSession ,user_id: int, number: int):
    try:
        user_number = VKUserNumber(
            id_user=user_id,
            number=number,
        )
        session.add(user_number)
        await session.commit()
    except Exception as e:
        log.info(f"Данные не коретны. Ошибка {e}")


async def get_user_number(session: AsyncSession, user_id: int, number: int | None = None):
    try:
        user_number = (await session.execute(
            select(VKUserNumber.number)
            .filter(or_(VKUserNumber.number == number, VKUserNumber.id_user == user_id))
            )).scalars().one_or_none()
        
        return user_number
    except Exception as e:
        log.info(f"Данные не коретны. Ошибка {e}")


async def is_mute_bot(session: AsyncSession ,user_id: int) -> bool:
    try:
        is_muth = (await session.execute(
            select(VKUser.muth)
            .filter(VKUser.vk_id == user_id)
            )).scalars().one_or_none()
        
        return is_muth
    except Exception as e:
        log.error(f"Ошбика при запросе {e}")


async def get_last_message(session: AsyncSession, user_id: int):
    try:
        message = (await session.execute(
            select(VKLastMessage.id_user)
            .filter(VKLastMessage.id_user == user_id)
            )).scalars().one_or_none()

        return message
    except Exception as e:
        log.error(f"Ошбика при запросе {e}")


async def del_last_message(session: AsyncSession, user_id: int):
    try:
        message_delete = (await session.execute(
            select(VKLastMessage)
            .filter(VKLastMessage.id_user == user_id)
            )).scalars().one_or_none()
        
        if message_delete is not None:
            await session.delete(message_delete)
            await session.commit()
    except Exception as e:
        log.error(f"Ошбика при удалении сообщения {e}")


async def put_last_message(session: AsyncSession, user_id: int, message_user: str):
    try:
        message = VKLastMessage(
            id_user = user_id,
            message = message_user,
        )
        session.add(message)
        await session.commit()
    except Exception as e:
        log.error(f"Ошибка при заполнении таблицы с соообщением {e}")
