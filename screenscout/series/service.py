from datetime import date

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from screenscout.country.models import Country
from screenscout.genre.models import Genre
from screenscout.language.models import Language
from screenscout.person.models import Person

from .models import Series, SeriesCreate, SeriesUpdate


async def get(*, db_session: AsyncSession, series_id: int) -> Series | None:
    """Returns a series based on the given id."""
    query = (
        select(Series)
        .where(Series.id == series_id)
        .options(selectinload(Series.country), selectinload(Series.genres))
    )
    result = await db_session.execute(query)

    return result.scalars().first()


async def get_all(
    *,
    db_session: AsyncSession,
    title: str | None = None,
    production_year: date | None = None,
    country_id: int | None = None,
    genre_id: int | None = None,
    min_rating: float | None = None,
    max_rating: float | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[Series]:
    """Return a paginated list of series with optional filters."""
    query = select(Series).options(
        selectinload(Series.country),
        selectinload(Series.genres),
        selectinload(Series.language),
        selectinload(Series.director),
    )

    filters = []

    if title:
        filters.append(Series.title.ilike(f"%{title}%"))

    if production_year:
        filters.append(Series.production_year == production_year)  # type: ignore

    if country_id:
        filters.append(Series.country.any(Country.id == country_id))  # type: ignore

    if genre_id:
        filters.append(Series.genres.any(Genre.id == genre_id))  # type: ignore

    if min_rating is not None:
        filters.append(Series.IMDb_rating >= min_rating)  # type: ignore

    if max_rating is not None:
        filters.append(Series.IMDb_rating <= max_rating)  # type: ignore

    if filters:
        query = query.where(and_(*filters))

    query = query.limit(limit).offset(offset)

    result = await db_session.execute(query)

    return result.scalars().all()  # type: ignore


async def create(*, db_session: AsyncSession, series_in: SeriesCreate) -> Series:
    """Creates a new series."""
    series_data = series_in.model_dump()
    country = series_data.pop("country")
    genres = series_data.pop("genres")
    languages = series_data.pop("language")
    director = series_data.pop("director")
    series = Series(**series_data)

    db_session.add(series)
    await db_session.commit()
    await db_session.refresh(series, ["country", "genres", "language", "director"])

    for country_id in country:
        result = await db_session.execute(
            select(Country).where(Country.id == country_id)
        )
        country = result.scalars().first()
        if country is not None:
            series.country.append(country)

    for genre_id in genres:
        result = await db_session.execute(select(Genre).where(Genre.id == genre_id))
        genre = result.scalars().first()
        if genre is not None:
            series.genres.append(genre)  # type: ignore

    for language_id in languages:
        result = await db_session.execute(
            select(Language).where(Language.id == language_id)
        )
        language = result.scalars().first()
        if language is not None:
            series.language.append(language)  # type: ignore

    for director_id in director:
        result = await db_session.execute(
            select(Person).where(Person.id == director_id)
        )
        director_db = result.scalars().first()
        if director_db is not None:
            series.director.append(director_db)  # type: ignore

    await db_session.commit()

    return series


async def update(
    *, db_session: AsyncSession, series: Series, series_in: SeriesUpdate
) -> Series:
    """Updates a series."""
    series_data = series.dict()
    update_data = series_in.model_dump(exclude_unset=True)
    for field in series_data:
        if field in update_data:
            setattr(series, field, update_data[field])

    if series_in.country is not None:
        series.country.clear()
        for country_id in series_in.country:
            result = await db_session.execute(
                select(Country).where(Country.id == country_id)
            )
            country = result.scalars().first()
            if country:
                series.country.append(country)

    if series_in.genres is not None:
        series.genres.clear()
        for genre_id in series_in.genres:
            result = await db_session.execute(select(Genre).where(Genre.id == genre_id))
            genre = result.scalars().first()
            if genre:
                series.genres.append(genre)  # type: ignore

    if series_in.language is not None:
        series.language.clear()
        for language_id in series_in.language:
            result = await db_session.execute(
                select(Language).where(Language.id == language_id)
            )
            language = result.scalars().first()
            if language:
                series.language.append(language)  # type: ignore

    if series_in.director is not None:
        series.director.clear()
        for director_id in series_in.director:
            result = await db_session.execute(
                select(Person).where(Person.id == director_id)
            )
            director_db = result.scalars().first()
            if director_db:
                series.director.append(director_db)  # type: ignore

    await db_session.commit()
    await db_session.refresh(series)

    return series


async def delete(*, db_session: AsyncSession, series_id: int) -> None:
    """Deletes an existing series."""
    result = await db_session.execute(select(Series).where(Series.id == series_id))
    series = result.scalars().first()
    await db_session.delete(series)
    await db_session.commit()
