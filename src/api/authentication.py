from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.exc import IntegrityError

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

from auth import (authenticate_user, create_access_token,
                      create_refresh_token, delete_tokens, get_password_hash)
from database import get_db
from models import Users
from schemas import UsersCreate, LoginUser


router = APIRouter(
    prefix="/auth"
)


@router.post("/register", status_code=201)
async def register_user(
    user: UsersCreate, db: Annotated["AsyncSession", Depends(get_db)]
):
    hashed_password = get_password_hash(user.password)
    new_user = Users(username=user.username, password=hashed_password, email=user.email)
    db.add(new_user)
    try:
        await db.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User already exists")


@router.post("/login")
async def login_user(
    user: LoginUser, db: Annotated["AsyncSession", Depends(get_db)]
):
    user = await authenticate_user(db, user.username, user.password)
    access_token = await create_access_token(db, user.id)
    refresh_token = await create_refresh_token(db, user.id, access_token)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.delete("/logout", status_code=204)
async def logout(access_token: str, db: Annotated["AsyncSession", Depends(get_db)]):
    await delete_tokens(db, access_token)


