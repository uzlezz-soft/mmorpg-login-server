from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.jwt import create_access_token, create_refresh_token, create_session_token
from app.schemas.user import Token, UserCreate, ServerJoinRequest
from app.crud.user import *
from app.crud.server import get_server_by_ip
from app.utils.security import verify_password
from app.services.ban_service import is_user_banned
from app.services.server_service import is_server_online
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timezone
from uuid import UUID

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

def register_user(db: Session, user: UserCreate) -> User:
    db_user = get_user_by_name(db, user.username) or get_user_by_email(db, user.email)
    if db_user:
        return None
    return create_user(db, user)

def user_sent_server_join_request(db: Session, user: User, data: ServerJoinRequest) -> bool | dict:
    if is_user_banned(db, user.id):
        return None
    server = get_server_by_ip(db, data.server_ip)
    if not server or not server.port == data.server_port:
        return False
    if not is_server_online(server):
        return False
    user.server_join_request = server.id
    user.server_join_request_time = datetime.now(timezone.utc)
    user.session_token = create_session_token({ 'user_id': str(user.id), 'server_id': str(server.id) })
    update_changes(db, user)
    return user.session_token

def update_users_on_server_shutdown(db: Session, server_id: UUID):
    disconnect_users(db, server_id)