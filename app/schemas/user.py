from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    refresh_token: str

class TokenData(BaseModel):
    username: str | None = None

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    email: str
    password: str

class UserLogin(UserBase):
    password: str