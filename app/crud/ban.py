from app.models.ban import Ban
import app.schemas.ban as schema
from app.crud.user import get_user_by_name
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from pytz import UTC

def get_bans_of_user(db: Session, user_id: UUID) -> List[Ban]:
    return db.query(Ban).filter(Ban.user_id == user_id).all()

def get_bans_of_all_users(db: Session) -> List[Ban]:
    return db.query(Ban).all()

def add_ban(db: Session, data: schema.BanNotification) -> Ban | None:
    db_user = get_user_by_name(db, data.username)
    if not db_user:
        return None
    try:
        banned_til = UTC.localize(data.banned_til)
    except:
        banned_til = data.banned_til
    db_ban = Ban(user_id=db_user.id, reason=data.reason, banned_til=banned_til, perma_ban=data.perma_ban)
    #if data.date:
    #    db_ban.date = data.date
    db.add(db_ban)
    db.commit()
    db.refresh(db_ban)
    return db_ban