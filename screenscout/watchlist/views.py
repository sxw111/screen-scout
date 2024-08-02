from fastapi import APIRouter, HTTPException, status

from screenscout.auth.service import CurrentUser
from screenscout.database.core import SessionDep
from screenscout.series.service import get as get_series
from screenscout.movie.service import get as get_movie
from screenscout.exceptions import EntityDoesNotExist, EntityAlreadyExists
from .service import (
    create_movie_watchlist_item,
    create_series_watchlist_item,
    get_user_watchlist,
    delete_watchlist_item,
)
from .models import MovieWatchlistRead, SeriesWatchlistRead, WatchlistRead


router = APIRouter()


@router.post("/movies/{movie_id}")
async def add_movie_to_watchlist(
    db_session: SessionDep,
    current_user: CurrentUser,
    movie_id: int,
):
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
    db_session: SessionDep,
    current_user: CurrentUser,
    series_id: int,
):
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
async def get_watchlist(db_session: SessionDep, current_user: CurrentUser):
    watchlist = await get_user_watchlist(db_session=db_session, user_id=current_user.id)

    watchlist_items = []

    for item in watchlist:
        if item["type"] == "movie":
            watchlist_items.append(MovieWatchlistRead(**item))
        elif item["type"] == "series":
            watchlist_items.append(SeriesWatchlistRead(**item))

    return WatchlistRead(watchlist=watchlist_items)


@router.delete("/{item_id}")
async def remove_from_watchlist(
    db_session: SessionDep,
    current_user: CurrentUser,
    item_id: int,
    item_type: str,
):
    await delete_watchlist_item(
        db_session=db_session,
        user_id=current_user.id,
        item_id=item_id,
        item_type=item_type,
    )
