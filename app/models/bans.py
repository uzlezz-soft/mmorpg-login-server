#from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from app.database import Base
from uuid import UUID

class Bans(Base):
    __tablename__ = "bans"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), index=True)
    reason: Mapped[str] = mapped_column()

    date: Mapped[DateTime] = mapped_column()
    banned_til: Mapped[DateTime] = mapped_column()
    perma_ban: Mapped[bool] = mapped_column()