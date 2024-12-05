from pydantic import BaseModel, EmailStr


class UsersCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    is_verified: bool | None = None


class UsersGet(UsersCreate):
    id: int


class LoginUser(BaseModel):
    username: str
    password: str
