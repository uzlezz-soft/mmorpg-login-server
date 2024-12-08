from sqlalchemy.orm import Session
from app.schemas.server import *
from app.models.server import Server
import app.crud.server as crud
from app.crud.user import get_user, get_user_by_name, update_changes
from app.config import settings
from datetime import datetime, timezone, timedelta
from app.utils.jwt import validate_session_token
from app.services.ban_service import is_user_banned
import pytz
# can't do from app.services.user_service import update_users_on_server_shutdown
# because it will cause chaos, and the world will end...
import app.services.user_service

def create_server(db: Session, data: ServerCreate, ip: str) -> ServerCreated | None:
    server = crud.get_server_by_ip(db, ip)
    if server:
        return None
    return crud.create_server(db, data, ip).id

def update_server_started(db: Session, data: ServerStarted, ip: str) -> bool:
    server = crud.get_server_by_ip(db, ip)
    if not server:
        return False
    crud.update_server_info_started(db, server, data)
    return True

def update_server(db: Session, data: ServerUpdate, ip: str) -> bool:
    server = crud.get_server_by_ip(db, ip)
    if not server:
        return False
    crud.update_server_info(db, server, data)
    return True

def is_server_online(server: Server) -> bool:
    difference = (datetime.now(timezone.utc) - pytz.UTC.localize(server.last_heartbeat)).total_seconds()
    return difference <= settings.SERVER_HEARTBEAT_TIMEOUT_SECONDS

def get_online_servers(db: Session, game_version: int):
    online_servers = [OnlineServer(**(x.__dict__)) for x in crud.get_servers(db, game_version) if is_server_online(x)]
    return OnlineServers(servers=online_servers)

def validate_user_join_request(db: Session, ip: str, data: JoinRequest) -> bool:
    user = get_user_by_name(db, data.username)
    if not user:
        return False
    if is_user_banned(db, user.id):
        return False
    if user.online_on_server:
        user_server = crud.get_server(db, user.online_on_server)
        if user_server and is_server_online(user_server) and user_server.players > 0:
            return False
    server = crud.get_server_by_ip(db, ip)
    if not server:
        return False
    if not user.server_join_request or not user.server_join_request_time or not user.session_token or user.server_join_request != server.id:
        return False
    if user.session_token != data.session_token:
        return False
    allowed_timeout = datetime.now(timezone.utc) - timedelta(seconds=settings.USER_JOIN_REQUEST_TIMEOUT_SECONDS)
    if pytz.UTC.localize(user.server_join_request_time) < allowed_timeout:
        return False
    token_data = validate_session_token(data.session_token)
    if not token_data:
        return False
    token_user = get_user(db, token_data['user_id'])
    token_server = crud.get_server(db, token_data['server_id'])
    if not token_user or not token_server or token_server.id != server.id or token_user.id != user.id:
        return False
    return True

def update_user_joined(db: Session, ip: str, data: UserJoined) -> bool:
    token = validate_session_token(data.session_token)
    if not token:
        return False
    server = crud.get_server(db, token['server_id'])
    if not server.ip == ip:
        return False
    user = get_user(db, token['user_id'])
    if is_user_banned(db, user.id):
        return False
    crud.update_server_with_heartbeat(db, server)
    user.online_on_server = server.id
    user.server_join_request = None
    update_changes(db, user)
    return True

def update_user_left(db: Session, ip: str, data: UserLeft):
    token = validate_session_token(data.session_token)
    if not token:
        return False
    server = crud.get_server(db, token['server_id'])
    if not server.ip == ip:
        return False
    user = get_user(db, token['user_id'])
    user.online_on_server = None
    user.session_token = None
    update_changes(db, user)
    crud.update_server_with_heartbeat(db, server)

def server_shutdown(db: Session, ip: str):
    server = crud.get_server_by_ip(db, ip)
    if not server:
        return False
    server.last_heartbeat = datetime.now(timezone.now) - timedelta(seconds=settings.SERVER_HEARTBEAT_TIMEOUT_SECONDS + 1)
    server.players = 0
    crud.update_server(db, server)
    app.services.user_service.update_users_on_server_shutdown(db, server.ip)