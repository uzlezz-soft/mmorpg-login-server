#from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column, Mapped
from app.database import Base
from uuid import uuid4, UUID

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()

    banned_til: Mapped[DateTime] = mapped_column()
    perma_ban: Mapped[bool] = mapped_column(default=False)

    playing: Mapped[bool] = mapped_column()