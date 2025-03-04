from pydantic import BaseModel

class PresentationCreate(BaseModel):
    name: str
    description: str


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserLogin(BaseModel):
    login: str
    password: str
