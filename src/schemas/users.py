from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class UserGet(UserCreate):
    id: int
