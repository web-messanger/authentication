import uuid
from datetime import datetime, timedelta
from fastapi import HTTPException, status

import bcrypt
import jwt
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models import AccessTokens, RefreshTokens, Users


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(
        password.encode(), settings.SECRET.PASSWORD_SALT.encode()
    ).decode()


async def authenticate_user(
    db: AsyncSession, username: str, password: str
) -> Users | None:
    query = select(Users).where(Users.username == username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if user and verify_password(password, user.password):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
    )


async def create_access_token(db: AsyncSession, user_id: int) -> str:
    now = datetime.utcnow()
    jwt_token = create_jwt(user_id, now)
    data = {"token": jwt_token, "user_id": user_id, "created_at": now}
    stmt = insert(AccessTokens).values(**data)
    await db.execute(stmt)
    await db.commit()
    return jwt_token


async def create_refresh_token(
    db: "AsyncSession", user_id: int, access_token: str
) -> str:
    expire = datetime.utcnow() + timedelta(
        seconds=settings.ACCEES_TOKEN.LIFETIME_SECONDS
    )
    jwt_token = str(uuid.uuid4())
    data = {"token": jwt_token, "access_token": access_token, "expires_at": expire}
    stmt = insert(RefreshTokens).values(**data)
    await db.execute(stmt)
    await db.commit()
    return jwt_token


def create_jwt(user_id: int, created_at: datetime) -> str:
    expire = created_at + timedelta(seconds=settings.ACCEES_TOKEN.LIFETIME_SECONDS)
    jwt_token = jwt.encode(
        {"sub": user_id, "exp": expire},
        settings.SECRET.VERIFICATION_TOKEN_SECRET,
        algorithm="HS256",
    )
    return jwt_token


async def delete_tokens(db: "AsyncSession", access_token: str) -> None:
    try:
        async with db.begin():
            stmt = delete(RefreshTokens).where(
                RefreshTokens.access_token == access_token
            )
            await db.execute(stmt)

            stmt = delete(AccessTokens).where(AccessTokens.token == access_token)
            await db.execute(stmt)
    except Exception:
        await db.rollback()
