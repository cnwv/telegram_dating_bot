from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, BigInteger, String, Boolean, null, ForeignKey

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, nullable=False)
    nickname = Column(String, nullable=True)
    premium = Column(Boolean, default=False)


class Messages(Base):
    __tablename__ = 'messages'
    user_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    message = Column(JSONB)

    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message


class Initial_Data(Base):
    __tablename__ = 'initial_data'
    user_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    data = Column(String)

    def __init__(self, user_id, data):
        self.user_id = user_id
        self.data = data
