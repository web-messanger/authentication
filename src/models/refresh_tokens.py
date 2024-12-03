from sqlalchemy import TIMESTAMP, Column, Text

from .base import Base


class RefreshTokens(Base):
    __tablename__ = "refresh_tokens"

    token = Column(Text, primary_key=True)
    access_token = Column(Text, nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
