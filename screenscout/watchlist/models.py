from datetime import datetime

from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column

from screenscout.database.core import Base
from screenscout.auth.models import User
from screenscout.movie.models import Movie
from screenscout.series.models import Series


class UserWatchlistMovieAssociation(Base):
    __tablename__ = "user_watchlist_movies"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    added_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="watchlist_movies")
    movie: Mapped["Movie"] = relationship(back_populates="users")


class UserWatchlistSeriesAssociation(Base):
    __tablename__ = "user_watchlist_series"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    series_id: Mapped[int] = mapped_column(ForeignKey("series.id"), primary_key=True)
    added_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="watchlist_series")
    series: Mapped["Series"] = relationship(back_populates="users")
