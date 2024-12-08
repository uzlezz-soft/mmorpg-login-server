from app.models.server import Server
from app.schemas.server import ServerCreate, ServerStarted, ServerUpdate
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, timezone, timedelta
from app.config import settings

def get_server(db: Session, id: UUID):
    return db.query(Server).filter(Server.id == id).first()

def get_server_by_ip(db: Session, ip: str):
    return db.query(Server).filter(Server.ip == ip).first()

def get_online_servers(db: Session):
    allowed_heartbeat = datetime.now(timezone.utc) - timedelta(seconds=settings.SERVER_HEARTBEAT_TIMEOUT_SECONDS)
    return db.query(Server).filter(Server.last_heartbeat >= allowed_heartbeat).all()

def get_servers(db: Session, game_version: int):
    return db.query(Server).filter(Server.game_version == game_version).all()

def update_server(db: Session, server: Server):
    db.commit()
    db.refresh(server)

def update_server_with_heartbeat(db: Session, server: Server):
    server.last_heartbeat = datetime.now(timezone.utc)
    update_server(db, server)

def create_server(db: Session, data: ServerCreate, ip: str):
    db_server = Server(**(data.__dict__), ip=ip, last_heartbeat=datetime.now(timezone.utc))
    db.add(db_server)
    update_server(db, db_server)
    return db_server

def update_server_info_started(db: Session, server: Server, data: ServerStarted):
    server.game_version = data.game_version
    server.port = data.port
    server.players = 0
    update_server_with_heartbeat(db, server)

def update_server_info(db: Session, server: Server, data: ServerUpdate):
    server.players = data.players
    update_server_with_heartbeat(db, server)