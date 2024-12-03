from sqlalchemy import Column, Integer, Text, Boolean

from .base import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(Text, unique=True)
    password = Column(Text)
    email = Column(Text, unique=True)
    is_verified = Column(Boolean, server_default="false")
