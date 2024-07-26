from pydantic import BaseModel


class CountryBase(BaseModel):
    name: str


class CountryCreate(CountryBase):
    pass


class CountryUpdate(CountryBase):
    pass


class CountryRead(CountryBase):
    id: int
