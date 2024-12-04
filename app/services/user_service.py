from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.jwt import create_access_token, create_refresh_token
from app.schemas.user import Token, TokenData
from app.schemas.user import UserCreate, UserLogin
from app.crud.user import get_user_by_email, get_user_by_name, create_user
from app.utils.security import verify_password
from fastapi.security import OAuth2PasswordRequestForm

def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = get_user_by_name(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def login_user(db: Session, user: OAuth2PasswordRequestForm):
    user = authenticate_user(db, user.username, user.password)
    if not user:
        return None
    payload = { 'username': user.username }
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)
    return Token(access_token=access_token, refresh_token=refresh_token)

def register_user(db: Session, user: UserCreate):
    db_user = get_user_by_name(db, user.username) or get_user_by_email(db, user.email)
    if db_user:
        return None
    return create_user(db, user)