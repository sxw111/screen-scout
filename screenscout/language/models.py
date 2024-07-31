from sqlalchemy.orm import Mapped, mapped_column

from screenscout.models import ScreenScoutBase
from screenscout.database.core import Base


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


class LanguageBase(ScreenScoutBase):
    name: str


class LanguageCreate(LanguageBase):
    pass


class LanguageUpdate(LanguageBase):
    pass


class LanguageRead(LanguageBase):
    id: int
