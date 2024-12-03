from datetime import datetime, timedelta
import jwt
import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from config import settings
from models import Users
from schemas import UsersGet

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), settings.SECRET.PASSWORD_SALT.encode()).decode()

async def authenticate_user(db: AsyncSession, username: str, password: str) -> Users | None:
    query = "SELECT * FROM users where username = :username"
    result = await db.execute(text(query), {"username": username})
    user = result.scalar_one_or_none()
    if user and verify_password(password, user.password):
        return user
    return None

async def create_access_token(db: AsyncSession, data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    now = datetime.utcnow()
    expire = now + (expires_delta or timedelta(seconds=settings.ACCEES_TOKEN.LIFETIME_SECONDS))
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(to_encode, settings.SECRET.VERIFICATION_TOKEN_SECRET, algorithm="HS256")

    stmt = "INSERT INTO access_tokens (token, user_id, created_at) VALUES (:token, :user_id, :created_at)"
    await db.execute(
        text(stmt),
        {
            "token": jwt_token,
            "user_id": to_encode.get("sub"),
            "created_at": now}
    )
    await db.commit()
    return jwt_token
