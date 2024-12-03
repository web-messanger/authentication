from sqlalchemy import Column, Text, TIMESTAMP

from .base import Base


class RefreshTokens(Base):
    __tablename__ = "refresh_tokens"

    token = Column(Text, primary_key=True)
    access_token = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
