from datetime import date

from sqlalchemy import ForeignKey, Column, Table, DATE
from sqlalchemy.orm import Mapped, mapped_column, relationship

from screenscout.core.db import Base
from screenscout.models.career_role import CareerRole
from screenscout.models.genre import Genre


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
    birthday: Mapped[date] = mapped_column(DATE, unique=False, nullable=True)
    career_roles: Mapped[list["CareerRole"]] = relationship(
        secondary=person_career_role_association
    )
    genres: Mapped[list["Genre"]] = relationship(secondary=person_genre_association)
