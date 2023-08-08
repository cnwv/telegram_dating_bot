from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, BigInteger, String, Boolean, ForeignKey, SmallInteger, DateTime

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, nullable=False)
    nickname = Column(String, nullable=True)
    premium = Column(Boolean, default=False)
    attempt = Column(SmallInteger, default=0)
    subscribe_expire_day = Column(DateTime, nullable=True, default=None)


class Messages(Base):
    __tablename__ = 'messages'
    user_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True, nullable=False)
    message = Column(JSONB, nullable=True, default=None)
    state = Column(SmallInteger, nullable=False, default=0)

    def __init__(self, user_id, message, state):
        self.user_id = user_id
        self.message = message
        self.state = state
