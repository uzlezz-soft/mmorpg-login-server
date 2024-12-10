from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
import app.schemas.ban as schema
from app.services.ban_service import *
from app.utils.security import validate_trusted_ip

router = APIRouter(prefix="/ban", tags=["ban"])

@router.get('/all', response_model=schema.BanList)
async def all(db: Session = Depends(get_db)):
    return get_all_bans(db)

@router.get('/all/{username}', response_model=schema.BanList)
async def all_of_users(username: str, db: Session = Depends(get_db)):
    bans = get_all_bans_of_user(db, username)
    if not bans:
        raise HTTPException(status_code=400, detail='Unknown user')
    return bans

@router.post('/notify', response_model=schema.BanRecord, dependencies=[Depends(validate_trusted_ip)])
async def notify(notification: schema.BanNotification, db: Session = Depends(get_db)):
    ban = add_ban(db, notification)
    if not ban:
        raise HTTPException(status_code=400, detail='Unknown user')
    return schema.BanRecord(**(ban.__dict__))