from datetime import date

from pydantic import BaseModel, Field

from screenscout.schemas.career_role import CareerRoleRead
from screenscout.schemas.genre import GenreRead


class PersonBase(BaseModel):
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


class PersonSeriesDirectorRead(BaseModel):
    id: int
    name: str
