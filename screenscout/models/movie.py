from datetime import date, datetime

from sqlalchemy import Column, Text, DECIMAL, Table, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from screenscout.core.db import Base
from screenscout.models.country import Country
from screenscout.models.genre import Genre


movie_genre_association = Table(
    "movie_genre",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id")),
    Column("genre_id", ForeignKey("genres.id")),
)

movie_country_association = Table(
    "movie_country",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id")),
    Column("country_id", ForeignKey("countries.id")),
)


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=False, nullable=False)
    release_date: Mapped[date] = mapped_column(unique=False, nullable=False)
    country: Mapped[list["Country"]] = relationship(secondary=movie_country_association)
    genres: Mapped[list["Genre"]] = relationship(secondary=movie_genre_association)
    rating: Mapped[float] = mapped_column(DECIMAL(3, 1), unique=False, nullable=False)
    description: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    director_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    age_category: Mapped[str] = mapped_column(unique=False, nullable=False)
    duration: Mapped[int] = mapped_column(unique=False, nullable=False)
    poster_url: Mapped[str] = mapped_column(unique=True, nullable=True)
    trailer_url: Mapped[str] = mapped_column(unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
