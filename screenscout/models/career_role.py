from sqlalchemy.orm import Mapped, mapped_column

from screenscout.core.db import Base


class CareerRole(Base):
    __tablename__ = "career_roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
