from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from screenscout.database.core import Base
from screenscout.models import ScreenScoutBase
from screenscout.movie.models import Movie
from screenscout.series.models import Series

if TYPE_CHECKING:
    from screenscout.auth.models import User


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


class MovieWatchlistRead(ScreenScoutBase):
    type: str = "movie"
    title: str
    added_at: datetime
    # details: dict


class SeriesWatchlistRead(ScreenScoutBase):
    type: str = "series"
    title: str
    added_at: datetime
    # details: dict


class WatchlistRead(ScreenScoutBase):
    watchlist: list[MovieWatchlistRead | SeriesWatchlistRead]
