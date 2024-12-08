from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from uuid import UUID

class CharacterCreate(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    class_type: int

class CharacterRecord(CharacterCreate):
    level: int
    experience: int

class UserCharacterList(BaseModel):
    characters: List[CharacterRecord]

class ServerCharacterLoadRequest(BaseModel):
    session_token: str

class ServerCharacterRecord(CharacterRecord):
    id: UUID
    inventory: list[dict]
    stats: list[dict]

class ServerCharacterList(BaseModel):
    characters: List[ServerCharacterRecord]

class CharacterDelete(BaseModel):
    name: str

class CharacterUpdate(BaseModel):
    session_token: str
    id: UUID
    level: int | None
    experience: int | None
    inventory: list[dict] | None
    stats: list[dict] | None

class CharactersUpdateRequest(BaseModel):
    updates: List[CharacterUpdate]