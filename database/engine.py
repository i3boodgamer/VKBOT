import sys
import os
import logging
from dotenv import load_dotenv
from pathlib import Path

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker


parent_dir = Path(__file__).resolve().parent.parent


from config import config


engine = create_engine(url=config.db_url, echo=False, pool_size=10, max_overflow=20)
session = sessionmaker(bind=engine, expire_on_commit=False)