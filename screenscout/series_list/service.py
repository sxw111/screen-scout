from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from screenscout.series.models import Series
from .models import SeriesList, SeriesListCreate, SeriesListUpdate


async def get(*, db_session: AsyncSession, series_list_id: int) -> SeriesList:
    query = (
        select(SeriesList)
        .where(SeriesList.id == series_list_id)
        .options(selectinload(SeriesList.series))
    )
    result = await db_session.execute(query)

    return result.scalars().first()


async def get_all(*, db_session: AsyncSession) -> list[SeriesList]:
    query = select(SeriesList).options(selectinload(SeriesList.series))
    result = await db_session.execute(query)

    return result.scalars().all()


async def create(*, db_session: AsyncSession, series_list_in: SeriesListCreate):
    series_list_data = series_list_in.model_dump()
    series = series_list_data.pop("series")
    series_list = SeriesList(**series_list_data)
    db_session.add(series_list)
    await db_session.commit()
    await db_session.refresh(series_list, ["series"])

    for series_id in series:
        result = await db_session.execute(select(Series).where(Series.id == series_id))
        series = result.scalars().first()
        if series is not None:
            series_list.series.append(series)

    await db_session.commit()


async def update(
    *,
    db_session: AsyncSession,
    series_list: SeriesList,
    series_list_in: SeriesListUpdate
) -> SeriesList:
    series_list_data = series_list.dict()
    update_data = series_list_in.model_dump(exclude_unset=True)

    for field in series_list_data:
        if field in update_data:
            setattr(series_list, field, update_data[field])

    if series_list_in.series is not None:
        series_list.series.clear()
        for series_id in series_list_in.series:
            result = await db_session.execute(
                select(Series).where(Series.id == series_id)
            )
            series = result.scalars().first()
            if series:
                series_list.series.append(series)

    await db_session.commit()
    await db_session.refresh(series_list)

    return series_list


async def delete(*, db_session: AsyncSession, series_list_id: int):
    result = await db_session.execute(
        select(SeriesList).where(SeriesList.id == series_list_id)
    )
    series_list = result.scalars().first()

    await db_session.delete(series_list)
    await db_session.commit()
