from app.models.character import Character
from app.schemas.character import *
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

def get_character(db: Session, id: UUID) -> Character:
    return db.query(Character).filter(Character.id == id).first()

def get_characters_of_user(db: Session, user_id: UUID) -> List[Character]:
    return db.query(Character).filter(Character.user_id == user_id).all()

def get_character_by_name(db: Session, name: str) -> Character:
    return db.query(Character).filter(Character.name == name).first()

def get_character_by_name_of_user(db: Session, name: str, user_id: UUID):
    return db.query(Character).filter(Character.user_id == user_id).filter(Character.name == name).first()

def add_character(db: Session, data: CharacterCreate, user_id: UUID) -> Character | None:
    db_character = Character(user_id=user_id, name=data.name, class_type=data.class_type)
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character

def delete_character(db: Session, character: Character):
    db.delete(character)
    db.commit()