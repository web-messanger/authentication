from sqlalchemy import Column, Integer, Text

from .base import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(Text, unique=True)
    password = Column(Text, unique=True)
    email = Column(Text, unique=True)
