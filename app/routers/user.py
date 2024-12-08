from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import login_user, register_user, user_sent_server_join_request
from app.schemas.user import UserBase, UserCreate, Token, ServerJoinRequest
from app.models.user import User
from app.utils.jwt import get_current_user

router = APIRouter(prefix="/user", tags=["user"])

@router.post('/register', response_model=UserBase)
async def register(request: UserCreate, db: Session = Depends(get_db)):
    token = register_user(db, request)
    if not token:
        raise HTTPException(status_code=400, detail='User with this email or name already exists')
    return token

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = login_user(db, form_data)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@router.post('/on_join_server')
async def on_join_server(data: ServerJoinRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = user_sent_server_join_request(db, user, data)
    if result == False:
        raise HTTPException(status_code=400, detail='Unknown server or is offline')
    elif result == None:
        raise HTTPException(status_code=403, detail='User is banned')
    return result