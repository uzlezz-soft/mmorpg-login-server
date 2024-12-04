from pydantic import BaseModel
from typing import List

class Ban(BaseModel):
    username: str
    reason: str
    is_perma_ban: bool

class BanList(BaseModel):
    bans: List[Ban]