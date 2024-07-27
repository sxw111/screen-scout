from datetime import date

from pydantic import BaseModel, Field

from screenscout.schemas.genre import GenreRead
from screenscout.schemas.country import CountryRead
from screenscout.schemas.language import LanguageRead


class MovieBase(BaseModel):
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
    title: str | None = None
    production_year: date | None = None
    IMDb_rating: float | None = None
    description: str | None = None
    age_category: str | None = None
    duration: int | None = None
    poster_url: str | None = None
    trailer_url: str | None = None
    country: list[int] | None = Field(default_factory=list)
    genres: list[int] | None = Field(default_factory=list)
    language: list[int] | None = Field(default_factory=list)
    director_id: int | None = None
    budget: int | None = None
    box_office: int | None = None


class MovieRead(MovieBase):
    id: int
    country: list[CountryRead]
    genres: list[GenreRead]
    language: list[LanguageRead]
