from datetime import datetime

from pydantic import EmailStr
from sqlalchemy import TIMESTAMP, Column, ForeignKey, func, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from screenscout.models import ScreenScoutBase
from screenscout.database.core import Base
from screenscout.watchlist.models import (
    UserWatchlistMovieAssociation,
    UserWatchlistSeriesAssociation,
)
from .enums import UserRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(unique=False, nullable=False)
    role: Mapped[UserRole] = mapped_column(default=UserRole.MEMBER)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    watchlist_movies: Mapped[list["UserWatchlistMovieAssociation"]] = relationship(
        back_populates="user"
    )
    watchlist_series: Mapped[list["UserWatchlistSeriesAssociation"]] = relationship(
        back_populates="user"
    )


class UserBase(ScreenScoutBase):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    username: str | None
    email: EmailStr | None
    password: str | None


class UserRead(UserBase):
    id: int
