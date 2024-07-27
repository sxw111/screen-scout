from fastapi import APIRouter, HTTPException, status

from screenscout.api.deps import SessionDep
from screenscout.crud.series import create, delete, get, get_all, update
from screenscout.schemas.series import SeriesCreate, SeriesRead, SeriesUpdate


router = APIRouter()


@router.get("/", response_model=list[SeriesRead])
async def get_all_series(db_session: SessionDep):
    """Return all series in the database."""
    return await get_all(db_session=db_session)


@router.get("/{series_id}", response_model=SeriesRead)
async def get_series(db_session: SessionDep, series_id: int):
    """Retrieve information about a series by its ID."""
    series = await get(db_session=db_session, series_id=series_id)
    if not series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Series with id `{series_id}` does not exist.",
        )

    return series


@router.post("/", response_model=SeriesRead)
async def create_series(db_session: SessionDep, series_in: SeriesCreate):
    """Create a new series."""
    series = await create(db_session=db_session, series_in=series_in)

    return series


@router.put("/{series_id}", response_model=SeriesRead)
async def update_series(db_session: SessionDep, series_id: int, series_in: SeriesUpdate):
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
async def delete_series(db_session: SessionDep, series_id: int):
    """Delete a series."""
    series = await get(db_session=db_session, series_id=series_id)
    if not series:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Series with id `{series_id}` does not exist.",
        )
    await delete(db_session=db_session, series_id=series_id)
