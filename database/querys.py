import logging

from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from .models import VKUser, VKUserPromocode, VKUserNumber


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


def get_user_table(session: Session, user_id: int) -> int:
    try:
        stmt = session.execute(
            select(VKUser.vk_id)
            .where(VKUser.vk_id == user_id)
        )
        
        return stmt.scalars().one_or_none()
    except Exception as e:
        log.error(f"Ошибка при запросе: {e}")


def get_user_table_promocode(session: Session, user_id: int) -> int:
    try:
        stmt = session.execute(
            select(VKUserPromocode.vk_id)
            .where(VKUserPromocode.vk_id == user_id)
        )
        return stmt.scalars().one_or_none()
    except Exception as e:
        log.error(f"Ошибка при запросе: {e}")


def add_user_table_promocode(session: Session, user_id: int):
    try:
        user=VKUserPromocode(
            vk_id=user_id,
            promocode=True,
        )
        session.add(user)
        session.commit()
    except Exception as e:
        log.info(f"Данные не коретны. Ошибка {e}")


def del_user_table(session: Session, user_id):
    user_delete = session.get(VKUser, user_id)

    if user_delete:
        session.delete(user_delete)
        session.commit()


def add_user_table(session: Session, user_id, name: str):
    try:
        user = VKUser(
            vk_id=user_id,
            name=name,
        )
        session.add(user)
        session.commit()
    except Exception as e:
        log.info(f"Данные не коретны. Ошибка {e}")


def mute_bot(session: Session, user_id: int):
    try:
        user: VKUser = session.execute(
            select(VKUser)
            .filter(VKUser.vk_id == user_id)
            ).scalars().one_or_none()
        user.muth = True
        
        session.add(user)
        session.commit()
    except Exception as e:
        log.error(f"Ошибка при коммите {e}")


def unmute_bot(session: Session, user_id: int):
    try:
        user: VKUser = session.execute(
            select(VKUser)
            .filter(VKUser.vk_id == user_id)
            ).scalars().one_or_none()
        log.info(user)
        user.muth = False
        
        session.add(user)
        session.commit()
    except Exception as e:
        log.error(f"Ошибка при коммите {e}")
    

def add_number(session: Session ,user_id: int, number: int):
    try:
        user_number = VKUserNumber(
            id_user=user_id,
            number=number,
        )
        session.add(user_number)
        session.commit()
    except Exception as e:
        log.info(f"Данные не коретны. Ошибка {e}")


def get_user_number(session: Session, user_id: int, number: int | None = None):
    try:
        user_number = session.execute(
            select(VKUserNumber.number)
            .filter(or_(VKUserNumber.number == number, VKUserNumber.id_user == user_id))
            ).scalars().one_or_none()
        
        return user_number
    except Exception as e:
        log.info(f"Данные не коретны. Ошибка {e}")


def is_mute_bot(session: Session ,user_id: int) -> bool:
    try:
        is_muth = session.execute(
            select(VKUser.muth)
            .filter(VKUser.vk_id == user_id)
            ).scalars().one_or_none()
        
        return is_muth
    except Exception as e:
        log.error(f"Ошбика при запросе {e}")

