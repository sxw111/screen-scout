from typing import Any

from fastapi import APIRouter, HTTPException, status

from screenscout.auth.models import User
from screenscout.auth.permissions import OwnerAdminManager
from screenscout.database.core import SessionDep

from .models import MovieListCreate, MovieListRead, MovieListUpdate
from .service import create, delete, get, get_all, update

router = APIRouter()


@router.get("/", response_model=list[MovieListRead])
async def get_movie_lists(db_session: SessionDep) -> Any:
    """Return all movie lists in the database."""
    movie_lists = await get_all(db_session=db_session)

    return movie_lists


@router.get("/{movie_list_id}", response_model=MovieListRead)
async def get_movie_list(db_session: SessionDep, movie_list_id: int) -> Any:
    """Retrieve information about a movie list by its ID."""
    movie_list = await get(db_session=db_session, movie_list_id=movie_list_id)
    if not movie_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie list with id `{movie_list_id}` does not exist.",
        )

    return movie_list


@router.post("/", response_model=MovieListRead)
async def create_movie_list(
    db_session: SessionDep,
    movie_list_in: MovieListCreate,
    current_user: User = OwnerAdminManager,
) -> Any:
    """Create a new movie list."""
    movie_list = await create(db_session=db_session, movie_list_in=movie_list_in)

    return movie_list


@router.put("/{movie_list_id}", response_model=MovieListRead)
async def update_movie_list(
    db_session: SessionDep,
    movie_list_id: int,
    movie_list_in: MovieListUpdate,
    current_user: User = OwnerAdminManager,
) -> Any:
    """Update a movie list."""
    movie_list = await get(db_session=db_session, movie_list_id=movie_list_id)
    if not movie_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie list with id `{movie_list_id}` does not exist.",
        )

    movie_list = await update(
        db_session=db_session, movie_list=movie_list, movie_list_in=movie_list_in
    )

    return movie_list


@router.delete("/{movie_list_id}", response_model=None)
async def delete_movie_list(
    db_session: SessionDep, movie_list_id: int, current_user: User = OwnerAdminManager
) -> None:
    """Delete a movie list."""
    movie_list = await get(db_session=db_session, movie_list_id=movie_list_id)
    if not movie_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie list with id `{movie_list_id}` does not exist.",
        )
    await delete(db_session=db_session, movie_list_id=movie_list_id)
