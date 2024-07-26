from sqlalchemy.orm import Mapped, mapped_column

from screenscout.core.db import Base


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
