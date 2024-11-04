from pathlib import Path

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

parent_dir = Path(__file__).resolve().parent.parent

from config import settings


engine = create_async_engine(url=settings.db_url, echo=False, pool_size=10, max_overflow=20)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)