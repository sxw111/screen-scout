from typing import Any

from fastapi import APIRouter, HTTPException, status
from fastapi_cache.decorator import cache

from screenscout.auth.models import User
from screenscout.auth.permissions import OwnerAdminManager
from screenscout.database.core import SessionDep

from .models import SeriesListCreate, SeriesListRead, SeriesListUpdate
from .service import create, delete, get, get_all, update

router = APIRouter()


@router.get("/", response_model=list[SeriesListRead])
@cache(expire=300)
async def get_series_lists(db_session: SessionDep) -> Any:
    """Return all series lists in the database."""
    series_lists = await get_all(db_session=db_session)

    return series_lists


@router.get("/{series_list_id}", response_model=SeriesListRead)
@cache(expire=300)
async def get_series_list(db_session: SessionDep, series_list_id: int) -> Any:
    """Retrieve information about a series list by its ID."""
    series_list = await get(db_session=db_session, series_list_id=series_list_id)
    if not series_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Series list with id `{series_list_id}` does not exist.",
        )

    return series_list


@router.post("/", response_model=SeriesListRead)
async def create_series_list(
    db_session: SessionDep,
    series_list_in: SeriesListCreate,
    current_user: User = OwnerAdminManager,
) -> Any:
    """Create a new series list."""
    series_list = await create(db_session=db_session, series_list_in=series_list_in)

    return series_list


@router.put("/{series_list_id}", response_model=SeriesListRead)
async def update_series_list(
    db_session: SessionDep,
    series_list_id: int,
    series_list_in: SeriesListUpdate,
    current_user: User = OwnerAdminManager,
) -> Any:
    """Update a series list."""
    series_list = await get(db_session=db_session, series_list_id=series_list_id)
    if not series_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Series list with id `{series_list_id}` does not exist.",
        )

    series_list = await update(
        db_session=db_session, series_list=series_list, series_list_in=series_list_in
    )

    return series_list


@router.delete("/{series_list_id}", response_model=None)
async def delete_series_list(
    db_session: SessionDep, series_list_id: int, current_user: User = OwnerAdminManager
) -> None:
    """Delete a series list."""
    series_list = await get(db_session=db_session, series_list_id=series_list_id)
    if not series_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Series list with id `{series_list_id}` does not exist.",
        )
    await delete(db_session=db_session, series_list_id=series_list_id)
