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

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(BigInteger, primary_key=True)
    messages = Column(JSONB)
