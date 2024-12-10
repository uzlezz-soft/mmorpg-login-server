from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.character import *
from app.utils.jwt import get_current_user
from app.services.character_service import *
from app.utils.security import validate_trusted_ip

router = APIRouter(prefix="/character", tags=["character"])

@router.post('/create')
async def create_c(data: CharacterCreate, user = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        result = create_character(db, data, user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    if result == None:
        raise HTTPException(status_code=416, detail='Character limit exceeded')
    if result == False:
        raise HTTPException(status_code=400, detail='Character with that name already exists')

@router.get('/my', response_model=UserCharacterList)
async def my_c(user = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_user_characters(db, user.id)

@router.post('/user', response_model=ServerCharacterList, dependencies=[Depends(validate_trusted_ip)])
async def of_user_s(data: ServerCharacterLoadRequest, request: Request, db: Session = Depends(get_db)):
    result = get_user_server_characters(db, data.session_token, request.client.host)
    if not result:
        raise HTTPException(status_code=400)
    return result

@router.delete('/delete')
async def delete_c(data: CharacterDelete, user = Depends(get_current_user), db: Session = Depends(get_db)):
    result = delete_user_character(db, data, user)
    if result == None:
        raise HTTPException(status_code=400)
    if result == False:
        # user is online on a server
        raise HTTPException(status_code=406)

@router.post('/update', dependencies=[Depends(validate_trusted_ip)])
async def update_s(data: CharactersUpdateRequest, request: Request, db: Session = Depends(get_db)):
    if not update_characters(db, data, request.client.host):
        raise HTTPException(status_code=400)