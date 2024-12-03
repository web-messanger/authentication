from sqlalchemy import TIMESTAMP, Column, Integer, Text

from .base import Base


class AccessTokens(Base):
    __tablename__ = "access_tokens"

    token = Column(Text, primary_key=True)
    user_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
