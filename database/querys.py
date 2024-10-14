import datetime
import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import VKUser, VKUserPromocode


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


def get_user_table(session: Session, user_id: int):
    stmt = session.execute(
        select(VKUser.vk_id)
        .where(VKUser.vk_id == user_id)
    )
    return stmt.scalars().all()


def get_user_table_promocode(session: Session, user_id: int):
    stmt = session.execute(
        select(VKUserPromocode.vk_id)
        .where(VKUserPromocode.vk_id == user_id)
    )
    return stmt.scalars().all()


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


def add_user_table(session: Session, user_id):
    try:
        user = VKUser(
            vk_id=user_id,
            created_by_id=1,
            created_at=datetime.datetime.now(),
            updated_by_id=1,
            updated_at=datetime.datetime.now()  # Убедитесь, что вы добавили updated_at
        )
        session.add(user)
        session.commit()
    except Exception as e:
        log.info(f"Данные не коретны. Ошибка {e}")

