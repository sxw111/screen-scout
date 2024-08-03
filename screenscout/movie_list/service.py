from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from screenscout.movie.models import Movie
from .models import MovieList, MovieListCreate, MovieListUpdate


async def get(*, db_session: AsyncSession, movie_list_id: int) -> MovieList:
    query = (
        select(MovieList)
        .where(MovieList.id == movie_list_id)
        .options(selectinload(MovieList.movies))
    )
    result = await db_session.execute(query)

    return result.scalars().first()


async def get_all(*, db_session: AsyncSession) -> list[MovieList]:
    query = select(MovieList).options(selectinload(MovieList.movies))
    result = await db_session.execute(query)

    return result.scalars().all()


async def create(*, db_session: AsyncSession, movie_list_in: MovieListCreate):
    movie_list_data = movie_list_in.model_dump()
    movies = movie_list_data.pop("movies")
    movie_list = MovieList(**movie_list_data)
    db_session.add(movie_list)
    await db_session.commit()
    await db_session.refresh(movie_list, ["movies"])

    for movie_id in movies:
        result = await db_session.execute(select(Movie).where(Movie.id == movie_id))
        movie = result.scalars().first()
        if movie is not None:
            movie_list.movies.append(movie)

    await db_session.commit()


async def update(
    *, db_session: AsyncSession, movie_list: MovieList, movie_list_in: MovieListUpdate
) -> MovieList:
    movie_list_data = movie_list.dict()
    update_data = movie_list_in.model_dump(exclude_unset=True)

    for field in movie_list_data:
        if field in update_data:
            setattr(movie_list, field, update_data[field])

    if movie_list_in.movies is not None:
        movie_list.movies.clear()
        for movie_id in movie_list_in.movies:
            result = await db_session.execute(select(Movie).where(Movie.id == movie_id))
            movie = result.scalars().first()
            if movie:
                movie_list.movies.append(movie)

    await db_session.commit()
    await db_session.refresh(movie_list)

    return movie_list


async def delete(*, db_session: AsyncSession, movie_list_id: int):
    result = await db_session.execute(
        select(MovieList).where(MovieList.id == movie_list_id)
    )
    movie_list = result.scalars().first()

    await db_session.delete(movie_list)
    await db_session.commit()
