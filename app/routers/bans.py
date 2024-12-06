from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
import app.schemas.bans as schema
from app.crud.ban import get_all_bans, add_ban

router = APIRouter(prefix="/bans", tags=["ban"])

@router.get('/all', response_model=schema.BanList)
def all(db: Session = Depends(get_db)):
    bans = map(lambda x: schema.Ban(**(x.__dict__)), get_all_bans(db))
    return schema.BanList(bans=bans)

@router.post('/notify', response_model=schema.BanRecord)
def notify(notification: schema.BanNotification, db: Session = Depends(get_db)):
    ban = add_ban(db, notification)
    if not ban:
        raise HTTPException(status_code=400, detail='User does not exist')
    return schema.BanRecord(**(ban.__dict__))