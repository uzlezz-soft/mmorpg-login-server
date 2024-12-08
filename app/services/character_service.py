from sqlalchemy.orm import Session
from app.models.character import Character
from app.schemas.character import *
from app.crud.character import *
from app.crud.server import get_server, get_server_by_ip
from app.utils.jwt import validate_session_token
from datetime import datetime, timezone
from app.config import settings
from uuid import UUID

def create_character(db: Session, data: CharacterCreate, user_id: UUID) -> bool | None:
    if len(get_characters_of_user(db, user_id)) >= settings.MAX_CHARACTERS_PER_USER:
        return None
    character = get_character_by_name(data.name)
    if character:
        return False
    create_character(db, data, user_id)
    return True

def get_user_characters(db: Session, user_id: UUID) -> UserCharacterList:
    return UserCharacterList(characters=map(lambda x: CharacterRecord(**(x.__dict__)), get_characters_of_user(user_id)))

def get_user_server_characters(db: Session, session_token: str, ip: str) -> ServerCharacterList | None:
    token = validate_session_token(session_token)
    if not token:
        return None
    server = get_server(db, token['server_id'])
    if not server.ip == ip:
        return None
    characters = get_characters_of_user(db, token['user_id'])
    return ServerCharacterList(characters=map(lambda x: ServerCharacterRecord(**(x.__dict__)), characters))

def delete_user_character(db: Session, data: CharacterDelete, user_id: UUID) -> bool:
    character = get_character_by_name_of_user(data.name, user_id)
    if not character:
        return None
    delete_character(db, character)
    return True

def update_characters(db: Session, data: CharactersUpdateRequest, ip: str) -> bool:
    server = get_server_by_ip(ip)
    if not server:
        return None
    for update in data.updates:
        token = validate_session_token(update.session_token)
        if not token:
            print(f'update_characters: session token is not valid')
            continue
        if token['server_id'] != ip:
            print(f'update_characters: server ips do not match -> rejecting request')
            return None
        character = get_character(db, update.id)
        if not character:
            continue
        if update.inventory is not None:
            character.inventory = update.inventory
        if update.stats is not None:
            character.stats = update.stats
    db.commit()
    print(f'update_characters: Processed {len(data.updates)} updates')
    return True