from pydantic import BaseModel


class GenreBase(BaseModel):
    name: str


class GenreCreate(GenreBase):
    pass


class GenreUpdate(GenreBase):
    pass


class GenreRead(GenreBase):
    id: int
