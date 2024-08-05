from sqlalchemy.orm import Mapped, mapped_column

from screenscout.database.core import Base
from screenscout.models import ScreenScoutBase


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


class CountryBase(ScreenScoutBase):
    name: str


class CountryCreate(CountryBase):
    pass


class CountryUpdate(CountryBase):
    pass


class CountryRead(CountryBase):
    id: int
