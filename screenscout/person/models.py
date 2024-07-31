from datetime import date

from pydantic import Field
from sqlalchemy import Column, DATE, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from screenscout.models import ScreenScoutBase
from screenscout.database.core import Base
from screenscout.career_role.models import CareerRole, CareerRoleRead
from screenscout.genre.models import Genre, GenreRead
from screenscout.movie.models import Movie


person_genre_association = Table(
    "person_genre",
    Base.metadata,
    Column("person_id", ForeignKey("persons.id")),
    Column("genre_id", ForeignKey("genres.id")),
)


person_career_role_association = Table(
    "person_career_role",
    Base.metadata,
    Column("person_id", ForeignKey("persons.id")),
    Column("career_role_id", ForeignKey("career_roles.id")),
)


class Person(Base):
    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=False, nullable=False)
    height: Mapped[int] = mapped_column(unique=False, nullable=True)
    directed_movies: Mapped[list[Movie]] = relationship()
    birthday: Mapped[date] = mapped_column(DATE, unique=False, nullable=True)
    career_roles: Mapped[list["CareerRole"]] = relationship(
        secondary=person_career_role_association
    )
    genres: Mapped[list["Genre"]] = relationship(secondary=person_genre_association)


class PersonBase(ScreenScoutBase):
    name: str
    height: int | None = None
    birthday: date | None = None


class PersonCreate(PersonBase):
    career_roles: list[int] | None = Field(default_factory=list)
    genres: list[int] | None = Field(default_factory=list)


class PersonUpdate(PersonBase):
    career_roles: list[int] | None = Field(default_factory=list)
    genres: list[int] | None = Field(default_factory=list)


class PersonRead(PersonBase):
    id: int
    career_roles: list[CareerRoleRead]
    genres: list[GenreRead]


class PersonSeriesDirectorRead(ScreenScoutBase):
    id: int
    name: str
