from datetime import datetime

from pydantic import BaseModel

from screenscout.schemas.career_role import CareerRoleRead
from screenscout.schemas.genre import GenreRead


class PersonBase(BaseModel):
    name: str
    height: int | None = None
    birthday: datetime | None = None


class PersonCreate(PersonBase):
    career: list[int] | None = []
    genres: list[int] | None = []


class PersonUpdate(PersonBase):
    career: list[int] | None = []
    genres: list[int] | None = []


class PersonRead(PersonBase):
    id: int
    career: list[CareerRoleRead]
    genres: list[GenreRead]
