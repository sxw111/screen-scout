from datetime import date
from typing import Any

from fastapi import APIRouter, HTTPException, Query, status
from fastapi_cache.decorator import cache

from screenscout.auth.models import User
from screenscout.auth.permissions import OwnerAdminManager
from screenscout.database.core import SessionDep
from screenscout.exceptions import EntityDoesNotExist

from .models import MovieCreate, MovieRead, MovieUpdate
from .service import create, delete, get, get_all, update

router = APIRouter()


@router.get("/", response_model=list[MovieRead])
@cache(expire=300)
async def get_movies(
    db_session: SessionDep,
    title: str | None = None,
    production_year: date | None = None,
    country_id: int | None = None,
    genre_id: int | None = None,
    min_rating: float | None = None,
    max_rating: float | None = None,
    limit: int = Query(20, gt=0),
    offset: int = Query(0, ge=0),
) -> Any:
    """Return all movies in the database with optional filters."""
    movies = await get_all(
        db_session=db_session,
        title=title,
        production_year=production_year,
        country_id=country_id,
        genre_id=genre_id,
        min_rating=min_rating,
        max_rating=max_rating,
        limit=limit,
        offset=offset,
    )
    return movies


@router.get("/{movie_id}", response_model=MovieRead)
@cache(expire=300)
async def get_movie(db_session: SessionDep, movie_id: int) -> Any:
    """Retrieve information about a movie by its ID."""
    movie = await get(db_session=db_session, movie_id=movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with id `{movie_id}` does not exist.",
        )

    return movie


@router.post("/", response_model=MovieRead)
async def create_movie(
    db_session: SessionDep,
    movie_in: MovieCreate,
    current_user: User = OwnerAdminManager,
) -> Any:
    """Create a new movie."""
    try:
        movie = await create(db_session=db_session, movie_in=movie_in)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id `{movie_in.director_id}` does not exist!",
        )

    return movie


@router.put("/{movie_id}", response_model=MovieRead)
async def update_movie(
    db_session: SessionDep,
    movie_id: int,
    movie_in: MovieUpdate,
    current_user: User = OwnerAdminManager,
) -> Any:
    """Update a movie."""
    movie = await get(db_session=db_session, movie_id=movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with id `{movie_id}` does not exist.",
        )

    movie = await update(db_session=db_session, movie=movie, movie_in=movie_in)

    return movie


@router.delete("/{movie_id}", response_model=None)
async def delete_movie(
    db_session: SessionDep, movie_id: int, current_user: User = OwnerAdminManager
) -> None:
    """Delete a movie."""
    movie = await get(db_session=db_session, movie_id=movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with id `{movie_id}` does not exist.",
        )
    await delete(db_session=db_session, movie_id=movie_id)
