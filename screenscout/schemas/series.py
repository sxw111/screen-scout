from datetime import date

from pydantic import BaseModel, Field

from screenscout.schemas.genre import GenreRead
from screenscout.schemas.country import CountryRead
from screenscout.schemas.language import LanguageRead
from screenscout.schemas.person import PersonSeriesDirectorRead


class SeriesBase(BaseModel):
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
