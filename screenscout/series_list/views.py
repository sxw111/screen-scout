from fastapi import APIRouter, HTTPException, status

from screenscout.database.core import SessionDep
from .models import SeriesListCreate, SeriesListUpdate, SeriesListRead
from .service import create, delete, get, get_all, update


router = APIRouter()


@router.get("/", response_model=list[SeriesListRead])
async def get_series_lists(db_session: SessionDep):
    """Return all series lists in the database."""
    series_lists = await get_all(db_session=db_session)

    return series_lists


@router.get("/{series_list_id}")
async def get_series_list(db_session: SessionDep, series_list_id: int):
    """Retrieve information about a series list by its ID."""
    series_list = await get(db_session=db_session, series_list_id=series_list_id)
    if not series_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Series list with id `{series_list_id}` does not exist.",
        )

    return series_list


@router.post("/", response_model=SeriesListRead)
async def create_series_list(db_session: SessionDep, series_list_in: SeriesListCreate):
    """Create a new series list.""" 
    series_list = await create(db_session=db_session, series_list_in=series_list_in)

    return series_list


@router.put("/{series_list_id}", response_model=SeriesListRead)
async def update_series_list(
    db_session: SessionDep, series_list_id: int, series_list_in: SeriesListUpdate
):
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
async def delete_series_list(db_session: SessionDep, series_list_id: int):
    """Delete a series list."""
    series_list = await get(db_session=db_session, series_list_id=series_list_id)
    if not series_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Series list with id `{series_list_id}` does not exist.",
        )
    await delete(db_session=db_session, series_list_id=series_list_id)
