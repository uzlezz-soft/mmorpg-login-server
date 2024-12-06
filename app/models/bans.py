from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import func
from app.database import Base
from uuid import UUID
from datetime import datetime
from typing import Optional

class Ban(Base):
    __tablename__ = "bans"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), index=True)
    reason: Mapped[str] = mapped_column(default='[not specified]')

    date: Mapped[datetime] = mapped_column(server_default=func.now())
    banned_til: Mapped[Optional[datetime]] = mapped_column()
    perma_ban: Mapped[bool] = mapped_column(default=False)