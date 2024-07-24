from fastapi import APIRouter, HTTPException, status

from screenscout.api.deps import SessionDep
from screenscout.schemas.country import CountryCreate, CountryRead, CountryUpdate
from screenscout.crud.country import get, get_all, create, update, delete, get_by_name


router = APIRouter()


@router.get("/", response_model=list[CountryRead])
async def get_countries(db_session: SessionDep):
    """Return all countries in the database."""
    return await get_all(db_session=db_session)


@router.get("/{country_id}", response_model=CountryRead)
async def get_country(db_session: SessionDep, country_id: int):
    """Retrieve information about a country by its ID."""
    country = await get(db_session=db_session, country_id=country_id)
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Country with id `{country_id}` does not exist.",
        )

    return country


@router.post("/", response_model=CountryRead)
async def create_country(db_session: SessionDep, country_in: CountryCreate):
    """Create a new country."""
    country = await get_by_name(db_session=db_session, name=country_in.name)
    if country:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Country with name `{country_in.name}` already exists.",
        )

    country = await create(db_session=db_session, country_in=country_in)

    return country


@router.put("/{country_id}", response_model=CountryRead)
async def update_country(
    db_session: SessionDep, country_id: int, country_in: CountryUpdate
):
    """Update a country."""
    country = await get(db_session=db_session, country_id=country_id)
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Country with id `{country_id}` does not exist.",
        )
    country = await update(
        db_session=db_session, country=country, country_in=country_in
    )

    return country


@router.delete("/{country_id}", response_model=None)
async def delete_country(db_session: SessionDep, country_id: int):
    """Delete a country."""
    country = await get(db_session=db_session, country_id=country_id)
    if not country:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Country with id `{country_id}` does not exist.",
        )
    await delete(db_session=db_session, country_id=country_id)
