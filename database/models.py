from datetime import datetime

from sqlalchemy import Integer, Column, TIMESTAMP, func, Boolean, ForeignKey, UniqueConstraint, BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id = Column(Integer, primary_key=True, autoincrement=True)


class VKUser(Base):
    __tablename__ = 'vk_users'

    vk_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, server_default=func.now())
    muth: Mapped[bool] = mapped_column(Boolean, default=False)


class VKUserPromocode(Base):
    __tablename__ = "vk_user_promocode"

    vk_id: Mapped[int] = mapped_column(ForeignKey("vk_users.vk_id"), primary_key=True)
    promocode: Mapped[bool] = mapped_column(Boolean)


class VKUserNumber(Base):
    __tablename__ = "vk_user_numbres"
    
    id_user: Mapped[int] = mapped_column(ForeignKey("vk_users.vk_id"), primary_key=True)
    number: Mapped[int] = mapped_column(BigInteger, nullable=False, primary_key=True, unique=True)


class VKLastMessage(Base):
    __tablename__ = "vk_last_messages"
    
    id_user: Mapped[int] = mapped_column(ForeignKey("vk_users.vk_id"), primary_key=True)
    message: Mapped[str] = mapped_column(String(10), nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, server_default=func.now())
    