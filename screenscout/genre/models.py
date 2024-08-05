from sqlalchemy.orm import Mapped, mapped_column

from screenscout.database.core import Base
from screenscout.models import ScreenScoutBase


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


class GenreBase(ScreenScoutBase):
    name: str


class GenreCreate(GenreBase):
    pass


class GenreUpdate(GenreBase):
    pass


class GenreRead(GenreBase):
    id: int
