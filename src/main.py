from sqlalchemy.exc import IntegrityError
from typing import TYPE_CHECKING, Annotated

from fastapi import FastAPI, Depends, HTTPException, status

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, engine
from models import Base, Users
from schemas import UsersCreate, UsersGet
from api.auth import get_password_hash, authenticate_user, create_access_token, create_refresh_token

app = FastAPI()


@app.post("/register", status_code=201)
async def register_user(user: UsersCreate, db: Annotated["AsyncSession", Depends(get_db)]):
    hashed_password = get_password_hash(user.password)
    new_user = Users(username=user.username, password=hashed_password, email=user.email)
    db.add(new_user)
    try:
        await db.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User already exists")

@app.post("/login")
async def login_user(username: str, password: str, db: Annotated["AsyncSession", Depends(get_db)]):
    user = await authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = await create_access_token(db, user.id)
    refresh_token = await create_refresh_token(db, user.id, access_token)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
