from pydantic import BaseModel


class UsersCreate(BaseModel):
    username: str
    password: str
    email: str

class UsersGet(UsersCreate):
    id: int
