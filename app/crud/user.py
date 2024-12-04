from app.models.user import User
from app.schemas.user import UserCreate, TokenData
from sqlalchemy.orm import Session
from app.utils.security import hash_password

def get_user(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()

def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.username == name).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_token_data(db: Session, data: TokenData):
    return db.query(User).filter(User.username == data.username).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(username = user.username, email=user.email, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user