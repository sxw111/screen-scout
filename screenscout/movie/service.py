from datetime import date

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from screenscout.exceptions import EntityDoesNotExist
from screenscout.movie.models import Movie, MovieCreate, MovieUpdate
from screenscout.country.models import Country
from screenscout.genre.models import Genre
from screenscout.language.models import Language
from screenscout.person.service import get as get_person


async def get(*, db_session: AsyncSession, movie_id: int) -> Movie | None:
    """Returns a movie based on the given id."""
    query = (
        select(Movie)
        .where(Movie.id == movie_id)
        .options(
            selectinload(Movie.country),
            selectinload(Movie.genres),
            selectinload(Movie.language),
        )
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
) -> list[Movie | None]:
    """Return a paginated list of movies with optional filters."""

    query = select(Movie).options(
        selectinload(Movie.country),
        selectinload(Movie.genres),
        selectinload(Movie.language),
    )

    filters = []

    if title:
        filters.append(Movie.title.ilike(f"%{title}%"))

    if production_year:
        filters.append(Movie.production_year == production_year)

    if country_id:
        filters.append(Movie.country.any(Country.id == country_id))

    if genre_id:
        filters.append(Movie.genres.any(Genre.id == genre_id))

    if min_rating is not None:
        filters.append(Movie.IMDb_rating >= min_rating)

    if max_rating is not None:
        filters.append(Movie.IMDb_rating <= max_rating)

    if filters:
        query = query.where(and_(*filters))

    query = query.limit(limit).offset(offset)

    result = await db_session.execute(query)

    return result.scalars().all()


async def create(*, db_session: AsyncSession, movie_in: MovieCreate) -> Movie:
    """Creates a new movie."""
    movie_data = movie_in.model_dump()
    director = await get_person(db_session=db_session, person_id=movie_in.director_id)
    if not director:
        raise EntityDoesNotExist(
            f"Person with id `{movie_in.director_id}` does not exist!"
        )
    country = movie_data.pop("country")
    genres = movie_data.pop("genres")
    languages = movie_data.pop("language")
    movie = Movie(**movie_data)
    db_session.add(movie)
    await db_session.commit()
    await db_session.refresh(movie, ["country", "genres", "language"])

    for country_id in country:
        result = await db_session.execute(
            select(Country).where(Country.id == country_id)
        )
        country = result.scalars().first()
        if country is not None:
            movie.country.append(country)

    for genre_id in genres:
        result = await db_session.execute(select(Genre).where(Genre.id == genre_id))
        genre = result.scalars().first()
        if genre is not None:
            movie.genres.append(genre)

    for language_id in languages:
        result = await db_session.execute(
            select(Language).where(Language.id == language_id)
        )
        language = result.scalars().first()
        if language is not None:
            movie.language.append(language)

    await db_session.commit()

    return movie


async def update(
    *, db_session: AsyncSession, movie: Movie, movie_in: MovieUpdate
) -> Movie:
    """Updates a movie."""
    movie_data = movie.dict()
    update_data = movie_in.model_dump(exclude_unset=True)

    for field in movie_data:
        if field in update_data:
            setattr(movie, field, update_data[field])

    if movie_in.country is not None:
        movie.country.clear()
        for country_id in movie_in.country:
            result = await db_session.execute(
                select(Country).where(Country.id == country_id)
            )
            country = result.scalars().first()
            if country:
                movie.country.append(country)

    if movie_in.genres is not None:
        movie.genres.clear()
        for genre_id in movie_in.genres:
            result = await db_session.execute(select(Genre).where(Genre.id == genre_id))
            genre = result.scalars().first()
            if genre:
                movie.genres.append(genre)

    if movie_in.language is not None:
        movie.language.clear()
        for language_id in movie_in.language:
            result = await db_session.execute(
                select(Language).where(Language.id == language_id)
            )
            language = result.scalars().first()
            if language:
                movie.language.append(language)

    await db_session.commit()
    await db_session.refresh(movie)

    return movie


async def delete(*, db_session: AsyncSession, movie_id: int):
    """Deletes an existing movie."""
    result = await db_session.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalars().first()

    await db_session.delete(movie)
    await db_session.commit()
