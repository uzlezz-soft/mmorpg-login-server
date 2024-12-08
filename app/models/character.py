from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import func
from sqlalchemy.types import JSON
from app.database import Base
from uuid import uuid4, UUID
from typing import Optional
from datetime import datetime

class Character(Base):
    __tablename__ = "characters"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    name: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    level: Mapped[int] = mapped_column(default=1)
    experience: Mapped[int] = mapped_column(default=0)
    class_type: Mapped[int] = mapped_column()
    
    inventory: Mapped[list[dict]] = mapped_column(JSON, default=list)
    stats: Mapped[list[dict]] = mapped_column(JSON, default=list)