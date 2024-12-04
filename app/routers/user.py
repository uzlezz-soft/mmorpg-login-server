from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import login_user, register_user
from app.schemas.user import UserBase, UserCreate, Token
from app.models.user import User
from app.utils.jwt import get_current_user

router = APIRouter(prefix="/user", tags=["user"])

@router.post('/register', response_model=UserBase)
def register(request: UserCreate, db: Session = Depends(get_db)):
    token = register_user(db, request)
    if not token:
        raise HTTPException(status_code=400, detail='User with this email or name already exists')
    return token

 #(request: UserLogin, db: Session = Depends(get_db)):
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = login_user(db, form_data)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user

@router.get('/me', summary='Get details of currently logged in user', response_model=UserBase)
async def get_me(user: User = Depends(get_current_user)):
    return user