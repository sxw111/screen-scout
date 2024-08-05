from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .models import Genre, GenreCreate, GenreUpdate


async def get(*, db_session: AsyncSession, genre_id: int) -> Genre | None:
    """Returns a genre based on the given id."""
    result = await db_session.execute(select(Genre).where(Genre.id == genre_id))

    return result.scalars().first()


async def get_by_name(*, db_session: AsyncSession, name: str) -> Genre | None:
    """Returns a genre by its name."""
    result = await db_session.execute(select(Genre).where(Genre.name == name))

    return result.scalars().first()


async def get_all(*, db_session: AsyncSession) -> list[Genre]:
    """Return all genres."""
    result = await db_session.execute(select(Genre))

    return result.scalars().all()  # type: ignore


async def create(*, db_session: AsyncSession, genre_in: GenreCreate) -> Genre:
    """Creates a new genre."""
    genre = Genre(**genre_in.model_dump())

    db_session.add(genre)
    await db_session.commit()
    await db_session.refresh(genre)

    return genre


async def update(
    *, db_session: AsyncSession, genre: Genre, genre_in: GenreUpdate
) -> Genre:
    """Updates a genre."""
    genre_data = genre.dict()
    update_data = genre_in.model_dump(exclude_unset=True)
    for field in genre_data:
        if field in update_data:
            setattr(genre, field, update_data[field])

    await db_session.commit()
    await db_session.refresh(genre)

    return genre


async def delete(*, db_session: AsyncSession, genre_id: int) -> None:
    """Deletes an existing genre."""
    result = await db_session.execute(select(Genre).where(Genre.id == genre_id))
    genre = result.scalars().first()
    await db_session.delete(genre)
    await db_session.commit()
