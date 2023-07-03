from db import schema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB
import asyncio


class Database:
    def __init__(self):
        self.engine = create_engine(DB.URL)
        schema.Base.metadata.create_all(bind=self.engine)
        self.maker = sessionmaker(bind=self.engine)




