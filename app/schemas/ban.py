from pydantic import BaseModel
from typing import List
from datetime import datetime
from uuid import UUID

class Ban(BaseModel):
    username: str
    reason: str
    perma_ban: bool
    date: datetime

class BanList(BaseModel):
    bans: List[Ban]

class BanNotification(Ban):
    banned_til: datetime | None

class BanRecord(BaseModel):
    user_id: UUID
    reason: str
    date: datetime
    banned_til: datetime | None
    perma_ban: bool