from datetime import date

from sqlalchemy import Column, Text, DECIMAL, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from screenscout.core.db import Base
from screenscout.models.country import Country
from screenscout.models.genre import Genre
from screenscout.models.language import Language
from screenscout.models.person import Person


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
    poster_url: Mapped[str] = mapped_column(unique=True, nullable=True)
    trailer_url: Mapped[str] = mapped_column(unique=True, nullable=True)
