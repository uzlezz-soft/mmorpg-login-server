from pydantic import BaseModel, Field, EmailStr

class Token(BaseModel):
    access_token: str
    refresh_token: str

class TokenData(BaseModel):
    username: str | None = None

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=16, pattern=r'^[a-zA-Z0-9_-]+$')

class UserCreate(UserBase):
    email: EmailStr
    password: str = Field(min_length=6, max_length=64)

class UserLogin(UserBase):
    password: str

class ServerJoinRequest(BaseModel):
    server_ip: str
    server_port: int

class SessionToken(BaseModel):
    session: str