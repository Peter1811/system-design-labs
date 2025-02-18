from pydantic import BaseModel

class Pres(BaseModel):
    name: str
    description: str


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str