from datetime import date

from pydantic import BaseModel, HttpUrl

from screenscout.schemas.genre import GenreRead
from screenscout.schemas.country import CountryRead


class MovieBase(BaseModel):
    title: str
    release_date: date
    rating: float
    description: str
    director_id: int
    age_category: str
    duration: int
    poster_url: HttpUrl | None = None
    trailer_url: HttpUrl | None = None


class MovieCreate(MovieBase):
    country: list[int]
    genres: list[int]
    director_id: int


class MovieUpdate(BaseModel):
    title: str | None = None
    release_date: date | None = None
    rating: float | None = None
    description: str | None = None
    age_category: str | None = None
    duration: int | None = None
    poster_url: HttpUrl | None = None
    trailer_url: HttpUrl | None = None
    country: list[int] | None = None
    genres: list[int] | None = None
    director_id: int | None = None


class MovieRead(MovieBase):
    id: int
    country: list[CountryRead]
    genres: list[GenreRead]
    director_id: int
