from datetime import date
from typing import Any

from fastapi import APIRouter, HTTPException, Query, status

from screenscout.auth.models import User
from screenscout.auth.permissions import OwnerAdminManager
from screenscout.database.core import SessionDep

from .models import SeriesCreate, SeriesRead, SeriesUpdate
from .service import create, delete, get, get_all, update

router = APIRouter()


@router.get("/", response_model=list[SeriesRead])
async def get_all_series(
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
    """Return a paginated list of series with optional filters."""
    series = await get_all(
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
    return series


@router.get("/{series_id}", response_model=SeriesRead)
async def get_series(db_session: SessionDep, series_id: int) -> Any:
    """Retrieve information about a series by its ID."""
    series = await get(db_session=db_session, series_id=series_id)
    if not series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Series with id `{series_id}` does not exist.",
        )

    return series


@router.post("/", response_model=SeriesRead)
async def create_series(
    db_session: SessionDep,
    series_in: SeriesCreate,
    current_user: User = OwnerAdminManager,
) -> Any:
    """Create a new series."""
    series = await create(db_session=db_session, series_in=series_in)

    return series


@router.put("/{series_id}", response_model=SeriesRead)
async def update_series(
    db_session: SessionDep,
    series_id: int,
    series_in: SeriesUpdate,
    current_user: User = OwnerAdminManager,
) -> Any:
    """Update a series."""
    series = await get(db_session=db_session, series_id=series_id)
    if not series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Series with id `{series_id}` does not exist.",
        )

    series = await update(db_session=db_session, series=series, series_in=series_in)

    return series


@router.delete("/{series_id}", response_model=None)
async def delete_series(
    db_session: SessionDep, series_id: int, current_user: User = OwnerAdminManager
) -> None:
    """Delete a series."""
    series = await get(db_session=db_session, series_id=series_id)
    if not series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Series with id `{series_id}` does not exist.",
        )
    await delete(db_session=db_session, series_id=series_id)
