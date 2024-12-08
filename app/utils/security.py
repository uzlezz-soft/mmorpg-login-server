from fastapi import Request, HTTPException
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password)

async def validate_trusted_ip(request: Request):
    ip = str(request.client.host)
    if ip not in settings.SERVER_TRUSTED_IPS:
        raise HTTPException(status_code=404)