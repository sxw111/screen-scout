from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from screenscout.models.movie import Movie
from screenscout.models.country import Country
from screenscout.models.genre import Genre
from screenscout.schemas.movie import MovieCreate, MovieUpdate


async def get(*, db_session: AsyncSession, movie_id):
    """Returns a movie based on the given id."""
    query = (
        select(Movie)
        .where(Movie.id == movie_id)
        .options(selectinload(Movie.country), selectinload(Movie.genres))
    )
    result = await db_session.execute(query)

    return result.scalars().first()


async def get_all(*, db_session: AsyncSession):
    """Return all movies."""
    query = select(Movie).options(
        selectinload(Movie.country), selectinload(Movie.genres)
    )
    result = await db_session.execute(query)

    return result.scalars().all()


async def create(*, db_session: AsyncSession, movie_in: MovieCreate):
    """Creates a new movie."""
    movie_data = movie_in.model_dump()
    country = movie_data.pop("country")
    genres = movie_data.pop("genres")
    movie = Movie(**movie_data)
    db_session.add(movie)
    await db_session.commit()
    await db_session.refresh(movie, ["country", "genres"])

    for country_id in country:
        result = await db_session.execute(
            select(Country).where(Country.id == country_id)
        )
        country = result.scalars().first()
        if country is not None:
            db_session.add(country)
        movie.country.append(country)

    for genre_id in genres:
        result = await db_session.execute(select(Genre).where(Genre.id == genre_id))
        genre = result.scalars().first()
        if genre is not None:
            db_session.add(genre)
        movie.genres.append(genre)

    await db_session.commit()

    return movie


async def update(*, db_session: AsyncSession, movie: Movie, movie_in: MovieUpdate):
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

    await db_session.commit()
    await db_session.refresh(movie)

    return movie


async def delete(*, db_session: AsyncSession, movie_id):
    """Deletes an existing movie."""
    result = await db_session.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalars().first()
    await db_session.delete(movie)
    await db_session.commit()
