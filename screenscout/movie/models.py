from datetime import date
from typing import TYPE_CHECKING

from pydantic import Field
from sqlalchemy import DECIMAL, Column, ForeignKey, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from screenscout.country.models import Country, CountryRead
from screenscout.database.core import Base
from screenscout.genre.models import Genre, GenreRead
from screenscout.language.models import Language, LanguageRead
from screenscout.models import ScreenScoutBase

if TYPE_CHECKING:
    from screenscout.watchlist.models import UserWatchlistMovieAssociation


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

movie_language_association = Table(
    "movie_language",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id")),
    Column("language_id", ForeignKey("languages.id")),
)


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=False, nullable=False)
    production_year: Mapped[date] = mapped_column(unique=False, nullable=False)
    country: Mapped[list["Country"]] = relationship(secondary=movie_country_association)
    language: Mapped[list["Language"]] = relationship(
        secondary=movie_language_association
    )
    genres: Mapped[list["Genre"]] = relationship(secondary=movie_genre_association)
    director_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    budget: Mapped[int] = mapped_column(unique=False, nullable=True)
    box_office: Mapped[int] = mapped_column(unique=False, nullable=True)
    IMDb_rating: Mapped[float] = mapped_column(
        DECIMAL(3, 1), unique=False, nullable=False
    )
    description: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    age_category: Mapped[str] = mapped_column(unique=False, nullable=False)
    duration: Mapped[int] = mapped_column(unique=False, nullable=False)
    poster_url: Mapped[str] = mapped_column(unique=False, nullable=True)
    trailer_url: Mapped[str] = mapped_column(unique=False, nullable=True)

    users: Mapped[list["UserWatchlistMovieAssociation"]] = relationship(
        back_populates="movie"
    )


class MovieBase(ScreenScoutBase):
    title: str
    production_year: date
    IMDb_rating: float
    description: str
    director_id: int
    age_category: str
    duration: int
    poster_url: str | None = None
    trailer_url: str | None = None
    budget: int | None = None
    box_office: int | None = None


class MovieCreate(MovieBase):
    country: list[int] | None = Field(default_factory=list)
    genres: list[int] | None = Field(default_factory=list)
    language: list[int] | None = Field(default_factory=list)


class MovieUpdate(MovieBase):
    title: str | None = None  # type: ignore
    production_year: date | None = None  # type: ignore
    IMDb_rating: float | None = None  # type: ignore
    description: str | None = None  # type: ignore
    age_category: str | None = None  # type: ignore
    duration: int | None = None  # type: ignore
    poster_url: str | None = None
    trailer_url: str | None = None
    country: list[int] | None = Field(default_factory=list)
    genres: list[int] | None = Field(default_factory=list)
    language: list[int] | None = Field(default_factory=list)
    director_id: int | None = None  # type: ignore
    budget: int | None = None
    box_office: int | None = None


class MovieRead(MovieBase):
    id: int
    country: list[CountryRead]
    genres: list[GenreRead]
    language: list[LanguageRead]
