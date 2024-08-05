from pydantic import Field
from sqlalchemy import Column, ForeignKey, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from screenscout.database.core import Base
from screenscout.models import ScreenScoutBase
from screenscout.series.models import Series

series_list_series_association = Table(
    "series_list_series",
    Base.metadata,
    Column("series_list_id", ForeignKey("series_lists.id")),
    Column("series_id", ForeignKey("series.id")),
)


class SeriesList(Base):
    __tablename__ = "series_lists"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    series: Mapped[list["Series"]] = relationship(
        secondary=series_list_series_association
    )

    @property
    def series_count(self) -> int:
        return len(self.series)


class SeriesListBase(ScreenScoutBase):
    name: str
    description: str


class SeriesListCreate(SeriesListBase):
    series: list[int] | None = Field(default_factory=list)


class SeriesListUpdate(SeriesListBase):
    name: str | None = None  # type: ignore
    description: str | None = None  # type: ignore
    series: list[int] | None = Field(default_factory=list)


class SeriesListRead(SeriesListBase):
    id: int
    series_count: int
