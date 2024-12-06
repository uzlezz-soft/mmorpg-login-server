from app.models.bans import Ban
import app.schemas.bans as schema
from app.crud.user import get_user_by_name
from sqlalchemy.orm import Session
from typing import List

def get_all_bans(db: Session) -> List[Ban]:
    return db.query(Ban).all()

def add_ban(db: Session, data: schema.BanNotification) -> Ban | None:
    db_user = get_user_by_name(db, data.username)
    if not db_user:
        return None
    db_ban = Ban(user_id=db_user.id, reason=data.reason, banned_til=data.banned_til, perma_ban=data.is_perma_ban)
    db.add(db_ban)
    db.commit()
    db.refresh(db_ban)
    return db_ban