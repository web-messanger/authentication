from pydantic import BaseModel


class UsersCreate(BaseModel):
    username: str
    password: str
    email: str

class UsersGet(UserCreate):
    id: int
