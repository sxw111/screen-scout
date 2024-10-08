from typing import Any

from fastapi import APIRouter, HTTPException, status

from screenscout.auth.models import User
from screenscout.auth.permissions import OwnerAdminManagerMember
from screenscout.database.core import SessionDep
from screenscout.exceptions import EntityAlreadyExists
from screenscout.movie.service import get as get_movie
from screenscout.series.service import get as get_series

from .models import MovieWatchlistRead, SeriesWatchlistRead, WatchlistRead
from .service import (
    create_movie_watchlist_item,
    create_series_watchlist_item,
    delete_watchlist_item,
    get_user_watchlist,
)

router = APIRouter()


@router.post("/movies/{movie_id}")
async def add_movie_to_watchlist(
    db_session: SessionDep, movie_id: int, current_user: User = OwnerAdminManagerMember
) -> dict[str, str]:
    """
    Adds a movie to the current user's watchlist.
    """
    movie = await get_movie(db_session=db_session, movie_id=movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with id `{movie_id}` does not exist.",
        )

    try:
        return await create_movie_watchlist_item(
            db_session=db_session, user_id=current_user.id, movie_id=movie_id
        )
    except EntityAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movie already in watchlist",
        )


@router.post("/series/{series_id}")
async def add_series_to_watchlist(
    db_session: SessionDep, series_id: int, current_user: User = OwnerAdminManagerMember
) -> dict[str, str]:
    """
    Adds a series to the current user's watchlist.
    """
    series = await get_series(db_session=db_session, series_id=series_id)
    if not series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Series with id `{series_id}` does not exist.",
        )

    try:
        return await create_series_watchlist_item(
            db_session=db_session, user_id=current_user.id, series_id=series_id
        )
    except EntityAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Series already in watchlist",
        )


@router.get("/", response_model=WatchlistRead)
async def get_watchlist(
    db_session: SessionDep, current_user: User = OwnerAdminManagerMember
) -> Any:
    """
    Retrieves the current user's watchlist.
    """
    watchlist = await get_user_watchlist(db_session=db_session, user_id=current_user.id)

    watchlist_items: list[MovieWatchlistRead | SeriesWatchlistRead] = []

    for item in watchlist:
        if item["type"] == "movie":
            watchlist_items.append(MovieWatchlistRead(**item))
        elif item["type"] == "series":
            watchlist_items.append(SeriesWatchlistRead(**item))

    return WatchlistRead(watchlist=watchlist_items)


@router.delete("/{item_id}")
async def remove_from_watchlist(
    db_session: SessionDep,
    item_id: int,
    item_type: str,
    current_user: User = OwnerAdminManagerMember,
) -> None:
    """
    Removes an item (movie or series) from the current user's watchlist.
    """
    await delete_watchlist_item(
        db_session=db_session,
        user_id=current_user.id,
        item_id=item_id,
        item_type=item_type,
    )
