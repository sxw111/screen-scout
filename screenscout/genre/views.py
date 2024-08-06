from typing import Any

from fastapi import APIRouter, HTTPException, status
from fastapi_cache.decorator import cache

from screenscout.auth.models import User
from screenscout.auth.permissions import OwnerAdminManager
from screenscout.database.core import SessionDep

from .models import GenreCreate, GenreRead, GenreUpdate
from .service import create, delete, get, get_all, get_by_name, update

router = APIRouter()


@router.get("/", response_model=list[GenreRead])
@cache(expire=3600)
async def get_genres(
    db_session: SessionDep, current_user: User = OwnerAdminManager
) -> Any:
    """Return all genres in the database."""
    return await get_all(db_session=db_session)


@router.get("/{genre_id}", response_model=GenreRead)
@cache(expire=3600)
async def get_genre(
    db_session: SessionDep, genre_id: int, current_user: User = OwnerAdminManager
) -> Any:
    """Retrieve information about a genre by its ID."""
    genre = await get(db_session=db_session, genre_id=genre_id)
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genre with id `{genre_id}` does not exist.",
        )

    return genre


@router.post("/", response_model=GenreRead)
async def create_genre(
    db_session: SessionDep,
    genre_in: GenreCreate,
    current_user: User = OwnerAdminManager,
) -> Any:
    """Create a new genre."""
    genre = await get_by_name(db_session=db_session, name=genre_in.name)
    if genre:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Genre with name `{genre_in.name}` already exists.",
        )

    genre = await create(db_session=db_session, genre_in=genre_in)

    return genre


@router.put("/{genre_id}", response_model=GenreRead)
async def update_genre(
    db_session: SessionDep,
    genre_id: int,
    genre_in: GenreUpdate,
    current_user: User = OwnerAdminManager,
) -> Any:
    """Update a genre."""
    genre = await get(db_session=db_session, genre_id=genre_id)
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genre with id `{genre_id}` does not exist.",
        )
    genre = await update(db_session=db_session, genre=genre, genre_in=genre_in)

    return genre


@router.delete("/{genre_id}", response_model=None)
async def delete_genre(
    db_session: SessionDep, genre_id: int, current_user: User = OwnerAdminManager
) -> None:
    """Delete a genre."""
    genre = await get(db_session=db_session, genre_id=genre_id)
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genre with id `{genre_id}` does not exist.",
        )
    await delete(db_session=db_session, genre_id=genre_id)
