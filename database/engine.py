import sys
import os
from dotenv import load_dotenv
from pathlib import Path

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker


parent_dir = Path(__file__).resolve().parent.parent


from config import config

engine = create_engine(url=config.db_url, echo=True)
session = sessionmaker(bind=engine, expire_on_commit=False)

metadata = MetaData()
vk_user_table = Table("vk_unsubscribes", metadata, autoload_with=engine)