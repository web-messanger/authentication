from pydantic import BaseModel, EmailStr


class UserEmail(BaseModel):
    email: EmailStr


class UsersCreate(UserEmail):
    username: str
    password: str
    is_verified: bool | None = None


class UsersGet(UsersCreate):
    id: int


class LoginUser(BaseModel):
    username: str
    password: str
