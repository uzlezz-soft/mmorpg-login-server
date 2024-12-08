from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import func
from app.database import Base
from uuid import uuid4, UUID
from typing import Optional
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    ban_id: Mapped[Optional[int]] = mapped_column()
    server_join_request: Mapped[Optional[UUID]] = mapped_column()
    server_join_request_time: Mapped[Optional[datetime]] = mapped_column()
    online_on_server: Mapped[Optional[UUID]] = mapped_column()
    session_token: Mapped[Optional[str]] = mapped_column()