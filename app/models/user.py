from sqlalchemy.orm import mapped_column, Mapped
from app.database import Base
from uuid import uuid4, UUID
from typing import Optional

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()

    ban_id: Mapped[Optional[int]] = mapped_column()
    playing: Mapped[bool] = mapped_column(default=False)