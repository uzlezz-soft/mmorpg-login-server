from sqlalchemy import CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import func
from app.database import Base
from uuid import uuid4, UUID
from datetime import datetime, timezone

class Server(Base):
    __tablename__ = "servers"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    game_version: Mapped[int] = mapped_column(default=0)
    ip: Mapped[str] = mapped_column(unique=True, index=True)
    port: Mapped[int] = mapped_column(CheckConstraint('port > 0 AND port <= 65535'))

    players: Mapped[int] = mapped_column(default=0)
    max_players: Mapped[int] = mapped_column()

    last_heartbeat: Mapped[datetime] = mapped_column(server_default=func.now())
    #mapped_column(default=lambda: datetime.now(timezone.utc))