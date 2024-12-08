from pydantic import BaseModel, Field
from typing import List
from uuid import UUID

class ServerCreate(BaseModel):
    name: str
    game_version: int = Field(ge=0)
    port: int = Field(gt=0, le=65535)
    max_players: int = Field(gt=0)

class ServerUpdate(BaseModel):
    players: int = Field(ge=0)

class ServerStarted(BaseModel):
    game_version: int = Field(ge=0)
    port: int = Field(gt=0, le=65535)

class ServerCreated(BaseModel):
    id: UUID

class OnlineServer(BaseModel):
    name: str
    ip: str
    port: int
    players: int
    max_players: int

class OnlineServers(BaseModel):
    servers: List[OnlineServer]

class JoinRequest(BaseModel):
    username: str
    session_token: str

class UserJoined(BaseModel):
    session_token: str

class UserLeft(BaseModel):
    session_token: str