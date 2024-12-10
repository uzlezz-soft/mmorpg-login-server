from sqlalchemy.orm import Session
from app.models.ban import Ban
from app.schemas.ban import *
from app.crud.ban import get_bans_of_all_users, get_bans_of_user, add_ban
from app.crud.user import get_user, get_user_by_name
from datetime import datetime, timezone
from uuid import UUID

def bans_to_schema(db: Session, bans: List[Ban]) -> BanList:
    return BanList(bans=map(lambda x: BanRecord(**(x.__dict__), username=get_user(db, x.user_id).username), bans))

def get_all_bans(db: Session) -> BanList:
    return bans_to_schema(db, get_bans_of_all_users(db))

def get_all_bans_of_user(db: Session, username: str) -> BanList:
    user = get_user_by_name(db, username)
    if not user:
        return None
    return bans_to_schema(db, get_bans_of_user(db, user.id))

def notify_ban(db: Session, data: BanNotification) -> Ban:
    return add_ban(db, data)

def is_user_banned(db: Session, user_id: UUID) -> bool:
    all_bans = get_bans_of_user(db, user_id)
    if not all_bans or len(all_bans) == 0:
        return False
    
    # iterate in reversed in case of user being banned
    # temporarily after permaban (this should not happed but still)
    for ban in reversed(all_bans):
        if ban.perma_ban:
            return True
        elif ban.banned_til > datetime.now(timezone.utc):
            return True
    return False