from pydantic import Field
from sqlalchemy import Column, ForeignKey, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from screenscout.database.core import Base
from screenscout.models import ScreenScoutBase
from screenscout.movie.models import Movie

movie_list_movie_association = Table(
    "movie_list_movie",
    Base.metadata,
    Column("movie_list_id", ForeignKey("movie_lists.id")),
    Column("movie_id", ForeignKey("movies.id")),
)


class MovieList(Base):
    __tablename__ = "movie_lists"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    movies: Mapped[list["Movie"]] = relationship(secondary=movie_list_movie_association)

    @property
    def movie_count(self) -> int:
        return len(self.movies)


class MovieListBase(ScreenScoutBase):
    name: str
    description: str


class MovieListCreate(MovieListBase):
    movies: list[int] | None = Field(default_factory=list)


class MovieListUpdate(MovieListBase):
    name: str | None = None  # type: ignore
    description: str | None = None  # type: ignore
    movies: list[int] | None = Field(default_factory=list)


class MovieListRead(MovieListBase):
    id: int
    movie_count: int
