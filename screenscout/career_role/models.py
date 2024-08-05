from sqlalchemy.orm import Mapped, mapped_column

from screenscout.database.core import Base
from screenscout.models import ScreenScoutBase


class CareerRole(Base):
    __tablename__ = "career_roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


class CareerRoleBase(ScreenScoutBase):
    name: str


class CareerRoleCreate(CareerRoleBase):
    pass


class CareerRoleUpdate(CareerRoleCreate):
    pass


class CareerRoleRead(CareerRoleCreate):
    id: int
