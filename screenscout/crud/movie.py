from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from screenscout.models.movie import Movie
from screenscout.models.country import Country
from screenscout.models.genre import Genre
from screenscout.schemas.movie import MovieCreate, MovieUpdate


async def get(*, db_session: AsyncSession, movie_id):
    """Returns a movie based on the given id."""
    result = await db_session.execute(select(Movie).where(Movie.id == movie_id))

    return result.scalars().first()


async def get_all(*, db_session: AsyncSession):
    """Return all movies."""
    result = await db_session.execute(select(Movie))

    return result.scalars().all()


async def create(*, db_session: AsyncSession, movie_in: MovieCreate):
    """Creates a new movie."""
    movie = Movie(*movie_in.model_dump())
    db_session.add(movie)
    await db_session.commit()
    await db_session.refresh(movie)

    if movie_in.country:
        for country_id in movie_in.country:
            result = await db_session.execute(
                select(Country).where(Country.id == country_id)
            )
            country = result.scalars().first()
            if country:
                movie.country.append(country)
        await db_session.commit()

    if movie_in.genres:
        for genre_id in movie_in.genres:
            result = await db_session.execute(select(Genre).where(Genre.id == genre_id))
            genre = result.scalars().first()
            if genre:
                movie.genres.append(genre)
        await db_session.commit()

    return movie


async def update(*, db_session: AsyncSession, movie: Movie, movie_in: MovieUpdate):
    """Updates a movie."""
    movie_data = movie.dict()
    update_data = movie_in.model_dump(skip_defaults=True)
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
