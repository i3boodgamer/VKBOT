from datetime import datetime

from sqlalchemy import Integer, Column, TIMESTAMP, func, Boolean
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True, autoincrement=True)


class VKUser(Base):
    __tablename__ = 'vk_unsubscribes'

    vk_id = Column(Integer)
    created_at = Column(TIMESTAMP, default=datetime.now, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=datetime.now)
    created_by_id = Column(Integer)
    updated_by_id = Column(Integer)

class VKUserPromocode(Base):
    __tablename__ = "vk_user_promocode"

    vk_id = Column(Integer)
    promocode = Column(Boolean)

