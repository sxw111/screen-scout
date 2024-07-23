from pydantic import BaseModel


class GenreCreate(BaseModel):
    name: str


class GenreRead(BaseModel):
    id: int
    name: str


class GenreUpdate(BaseModel):
    name: str
