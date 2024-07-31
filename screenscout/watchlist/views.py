from fastapi import APIRouter, HTTPException, status

from screenscout.auth.service import CurrentUser
from screenscout.database.core import SessionDep
from screenscout.movie.models import Movie
from screenscout.movie.service import get as get_movie

from .service import create_movie_watchlist_item


router = APIRouter()


@router.post("/{movie_id}")
async def add_movie_to_watchlist(
    db_session: SessionDep, current_user: CurrentUser, movie_id: int
):
    return await create_movie_watchlist_item(
        db_session=db_session, user_id=current_user.id, movie_id=movie_id
    )
