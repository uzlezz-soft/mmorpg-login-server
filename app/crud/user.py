from app.models.user import User
from app.schemas.user import UserCreate
from sqlalchemy import update
from sqlalchemy.orm import Session
from app.utils.security import hash_password
from uuid import UUID

def get_user(db: Session, id: UUID):
    return db.query(User).filter(User.id == id).first()

def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.username == name).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def update_changes(db: Session, user: User):
    db.commit()
    return user

def disconnect_users(db: Session, server_id: UUID):
    update(User).where(User.online_on_server == server_id).values(online_on_server = None, session_token = None)

def create_user(db: Session, user: UserCreate):
    db_user = User(username = user.username, email=user.email, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user