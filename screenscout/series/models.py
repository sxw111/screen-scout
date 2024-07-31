from datetime import date

from pydantic import Field
from sqlalchemy import Column, DECIMAL, ForeignKey, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from screenscout.models import ScreenScoutBase
from screenscout.database.core import Base
from screenscout.country.models import Country, CountryRead
from screenscout.genre.models import Genre, GenreRead
from screenscout.language.models import Language, LanguageRead
from screenscout.person.models import Person, PersonSeriesDirectorRead
from screenscout.watchlist.models import UserWatchlistSeriesAssociation


series_genre_association = Table(
    "series_genre",
    Base.metadata,
    Column("series_id", ForeignKey("series.id")),
    Column("genre_id", ForeignKey("genres.id")),
)

series_country_association = Table(
    "series_country",
    Base.metadata,
    Column("series_id", ForeignKey("series.id")),
    Column("country_id", ForeignKey("countries.id")),
)


series_language_association = Table(
    "series_language",
    Base.metadata,
    Column("series_id", ForeignKey("series.id")),
    Column("language_id", ForeignKey("languages.id")),
)


series_director_association = Table(
    "series_director",
    Base.metadata,
    Column("series_id", ForeignKey("series.id")),
    Column("director_id", ForeignKey("persons.id")),
)


class Series(Base):
    __tablename__ = "series"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=False, nullable=False)
    production_year: Mapped[date] = mapped_column(unique=False, nullable=False)
    country: Mapped[list["Country"]] = relationship(
        secondary=series_country_association
    )
    language: Mapped[list["Language"]] = relationship(
        secondary=series_language_association
    )
    seasons_count: Mapped[int] = mapped_column(unique=False, nullable=False)
    genres: Mapped[list["Genre"]] = relationship(secondary=series_genre_association)
    director: Mapped[list["Person"]] = relationship(
        secondary=series_director_association
    )
    IMDb_rating: Mapped[float] = mapped_column(
        DECIMAL(3, 1), unique=False, nullable=False
    )
    description: Mapped[str] = mapped_column(Text, unique=False, nullable=False)
    age_category: Mapped[str] = mapped_column(unique=False, nullable=False)
    poster_url: Mapped[str] = mapped_column(unique=False, nullable=True)
    trailer_url: Mapped[str] = mapped_column(unique=False, nullable=True)

    users: Mapped[list["UserWatchlistSeriesAssociation"]] = relationship(
        back_populates="series"
    )


class SeriesBase(ScreenScoutBase):
    title: str
    production_year: date
    IMDb_rating: float
    seasons_count: int
    description: str
    age_category: str
    poster_url: str | None = None
    trailer_url: str | None = None


class SeriesCreate(SeriesBase):
    country: list[int] | None = Field(default_factory=list)
    genres: list[int] | None = Field(default_factory=list)
    language: list[int] | None = Field(default_factory=list)
    director: list[int] | None = Field(default_factory=list)


class SeriesUpdate(SeriesBase):
    title: str | None = None
    production_year: date | None = None
    IMDb_rating: float | None = None
    seasons_count: int | None = None
    description: str | None = None
    age_category: str | None = None
    poster_url: str | None = None
    trailer_url: str | None = None
    country: list[int] | None = Field(default_factory=list)
    genres: list[int] | None = Field(default_factory=list)
    language: list[int] | None = Field(default_factory=list)
    director: list[int] | None = Field(default_factory=list)


class SeriesRead(SeriesBase):
    id: int
    country: list[CountryRead]
    genres: list[GenreRead]
    language: list[LanguageRead]
    director: list[PersonSeriesDirectorRead]
