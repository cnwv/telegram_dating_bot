from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, BigInteger, String, Boolean, ForeignKey, null

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, nullable=False)
    nickname = Column(String, nullable=True)
    premium = Column(Boolean, default=False)


class Messages(Base):
    __tablename__ = 'messages'
    user_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True, nullable=False)
    message = Column(JSONB, nullable=True, default=None)
    is_online = Column(Boolean, nullable=True, default=None)

    def __init__(self, user_id, message, is_online):
        self.user_id = user_id
        self.message = message
        self.is_online = is_online
