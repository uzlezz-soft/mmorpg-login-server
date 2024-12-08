from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.server_service import *
from app.schemas.server import *
from app.utils.security import validate_trusted_ip

router = APIRouter(prefix="/server", tags=["server"])

@router.post("/create", response_model=ServerCreated, dependencies=[Depends(validate_trusted_ip)])
async def create(data: ServerCreate, request: Request, db: Session = Depends(get_db)):
    ip = request.client.host
    server = create_server(db, data, ip)
    if not server:
        raise HTTPException(status_code=400)
    return ServerCreated(id=server)

@router.post("/on_started", dependencies=[Depends(validate_trusted_ip)])
async def on_started(data: ServerStarted, request: Request, db: Session = Depends(get_db)):
    ip = request.client.host
    if not update_server_started(db, data, ip):
        raise HTTPException(status_code=404)

@router.post("/update", dependencies=[Depends(validate_trusted_ip)])
async def update(data: ServerUpdate, request: Request, db: Session = Depends(get_db)):
    ip = request.client.host
    if not update_server(db, data, ip):
        raise HTTPException(status_code=404)

@router.get("/online/{game_version}", response_model=OnlineServers)
async def online(game_version: int, db: Session = Depends(get_db)):
    return get_online_servers(db, game_version)

@router.post("/validate_join_request", dependencies=[Depends(validate_trusted_ip)])
async def validate_join_request(data: JoinRequest, request: Request, db: Session = Depends(get_db)):
    if not validate_user_join_request(db, request.client.host, data):
        raise HTTPException(status_code=401)

@router.post("/on_user_joined", dependencies=[Depends(validate_trusted_ip)])
async def on_user_joined(data: UserJoined, request: Request, db: Session = Depends(get_db)):
    if not update_user_joined(db, request.client.host, data):
        raise HTTPException(status_code=401)

@router.post("/on_user_left", dependencies=[Depends(validate_trusted_ip)])
async def on_user_left(data: UserLeft, request: Request, db: Session = Depends(get_db)):
    update_user_left(db, request.client.host, data)

@router.post("/on_shutdown", dependencies=[Depends(validate_trusted_ip)])
async def on_shutdown(request: Request, db: Session = Depends(get_db)):
    server_shutdown(db, request.client.host)