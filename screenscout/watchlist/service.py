from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import exists
from sqlalchemy.orm import selectinload


from screenscout.auth.models import User

from screenscout.exceptions import EntityAlreadyExists
from .models import UserWatchlistMovieAssociation, UserWatchlistSeriesAssociation


async def create_movie_watchlist_item(
    db_session: AsyncSession, user_id: int, movie_id: int
):
    query = select(
        exists().where(
            UserWatchlistMovieAssociation.user_id == user_id,
            UserWatchlistMovieAssociation.movie_id == movie_id,
        )
    )

    result = await db_session.execute(query)
    exists_in_watchlist = result.scalar()

    if exists_in_watchlist:
        raise EntityAlreadyExists("Movie arleady in watchlist")

    new_entry = UserWatchlistMovieAssociation(user_id=user_id, movie_id=movie_id)

    db_session.add(new_entry)
    await db_session.commit()

    return {"message": "Movie added to watchlist successfully"}


async def create_series_watchlist_item(
    db_session: AsyncSession, user_id: int, series_id: int
):
    query = select(
        exists().where(
            UserWatchlistSeriesAssociation.user_id == user_id,
            UserWatchlistSeriesAssociation.series_id == series_id,
        )
    )

    result = await db_session.execute(query)
    exists_in_watchlist = result.scalar()

    if exists_in_watchlist:
        raise EntityAlreadyExists("Movie arleady in watchlist")

    new_entry = UserWatchlistSeriesAssociation(user_id=user_id, series_id=series_id)

    db_session.add(new_entry)
    await db_session.commit()

    return {"message": "Series added to watchlist successfully"}


async def get_user_watchlist(
    db_session: AsyncSession, user_id: int
) -> list[dict[str, any]]:
    result = await db_session.execute(
        select(User)
        .options(
            selectinload(User.watchlist_movies).selectinload(
                UserWatchlistMovieAssociation.movie
            ),
            selectinload(User.watchlist_series).selectinload(
                UserWatchlistSeriesAssociation.series
            ),
        )
        .where(User.id == user_id)
    )
    user = result.scalars().first()

    watchlist = []
    if user:
        for assoc in user.watchlist_movies:
            watchlist.append(
                {
                    "type": "movie",
                    "title": assoc.movie.title,
                    "added_at": assoc.added_at,
                    # "details": assoc.movie,
                }
            )

        for assoc in user.watchlist_series:
            watchlist.append(
                {
                    "type": "series",
                    "title": assoc.series.title,
                    "added_at": assoc.added_at,
                    # "details": assoc.series,
                }
            )

        watchlist.sort(key=lambda x: x["added_at"])

    return watchlist


async def delete_watchlist_item(
    db_session: AsyncSession,
    user_id: int,
    item_id: int,
    item_type: str,
) -> None:
    try:
        if item_type == "movie":
            assoc_result = await db_session.execute(
                select(UserWatchlistMovieAssociation)
                .where(UserWatchlistMovieAssociation.user_id == user_id)
                .where(UserWatchlistMovieAssociation.movie_id == item_id)
            )
            association = assoc_result.scalars().one()
        elif item_type == "series":
            assoc_result = await db_session.execute(
                select(UserWatchlistSeriesAssociation)
                .where(UserWatchlistSeriesAssociation.user_id == user_id)
                .where(UserWatchlistSeriesAssociation.series_id == item_id)
            )
            association = assoc_result.scalars().one()
        else:
            raise ValueError("Invalid item type")

        await db_session.delete(association)
        await db_session.commit()
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in watchlist"
        )
