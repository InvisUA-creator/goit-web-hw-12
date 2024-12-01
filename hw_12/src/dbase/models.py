from datetime import date
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Date, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contact"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(16), nullable=False)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    data_add: Mapped[Optional[str]] = mapped_column(String(250))
    created_at: Mapped[date] = mapped_column(
        "created_at", DateTime, default=func.now(), nullable=True
    )
    updated_at: Mapped[date] = mapped_column(
        "updated_at", DateTime, default=func.now(), onupdate=func.now(), nullable=True
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=True)
    user: Mapped["User"] = relationship("User", backref="contact", lazy="joined")


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[date] = mapped_column(
        "created_at", DateTime, default=func.now(), nullable=True
    )
    updated_ut: Mapped[date] = mapped_column(
        "updated_at", DateTime, default=func.now(), onupdate=func.now()
    )
