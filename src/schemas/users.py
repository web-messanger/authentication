from pydantic import BaseModel


class UsersCreate(BaseModel):
    username: str
    password: str
    email: str
    is_verified: bool


class UsersGet(UsersCreate):
    id: int
