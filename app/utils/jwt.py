from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app.database import get_db
from pydantic import ValidationError
from app.models.user import User
from app.crud.user import get_user_by_name
from app.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from uuid import UUID

def _create_json_web_token(data: dict, expires_delta: timedelta, secret: str):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({ 'exp': expire })
    return jwt.encode(to_encode, secret, algorithm=settings.ALGORITHM)

def create_access_token(data: dict):
    return _create_json_web_token(data, timedelta(minutes=settings.JWT_TIMEOUT_MINUTES), settings.SECRET_KEY)

def create_refresh_token(data: dict):
    return _create_json_web_token(data, timedelta(minutes=settings.JWT_REFRESH_TIMEOUT_MINUTES), settings.REFRESH_SECRET_KEY)

def create_session_token(data: dict):
    return _create_json_web_token(data, timedelta(minutes=settings.SESSION_TIMEOUT_MINUTES), settings.SESSION_SECRET_KEY)

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/user/login",
    scheme_name="JWT"
)

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(reuseable_oauth)) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        if datetime.fromtimestamp(payload['exp']) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_name(db, payload['username'])
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find user")
    return user

def validate_session_token(token: str):
    try:
        payload = jwt.decode(token, settings.SESSION_SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return { 'user_id': UUID(payload['user_id']), 'server_id': UUID(payload['server_id']) }