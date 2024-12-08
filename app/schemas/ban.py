from pydantic import BaseModel
from typing import List
from datetime import datetime
from uuid import UUID

class BanRecord(BaseModel):
    username: str
    reason: str
    perma_ban: bool
    date: datetime

class BanList(BaseModel):
    bans: List[BanRecord]

class BanNotification(BanRecord):
    banned_til: datetime | None

class FullBanRecord(BaseModel):
    user_id: UUID
    reason: str
    date: datetime
    banned_til: datetime | None
    perma_ban: bool