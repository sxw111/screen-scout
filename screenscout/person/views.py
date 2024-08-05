from fastapi import APIRouter, HTTPException, status

from screenscout.database.core import SessionDep
from .models import PersonCreate, PersonRead, PersonUpdate
from .service import create, delete, get, get_all, update

from screenscout.auth.permissions import OwnerAdminManager
from screenscout.auth.models import User


router = APIRouter()


@router.get("/", response_model=list[PersonRead])
async def get_persons(db_session: SessionDep):
    """Return all persons in the database."""
    return await get_all(db_session=db_session)


@router.get("/{person_id}", response_model=PersonRead)
async def get_person(db_session: SessionDep, person_id: int):
    """Retrieve information about a person by its ID."""
    person = await get(db_session=db_session, person_id=person_id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id `{person_id}` does not exist.",
        )

    return person


@router.post("/", response_model=PersonRead)
async def create_person(
    db_session: SessionDep,
    person_in: PersonCreate,
    current_user: User = OwnerAdminManager,
):
    """Create a new person."""
    person = await create(db_session=db_session, person_in=person_in)

    return person


@router.put("/{person_id}", response_model=PersonRead)
async def update_person(
    db_session: SessionDep,
    person_id: int,
    person_in: PersonUpdate,
    current_user: User = OwnerAdminManager,
):
    """Update a person."""
    person = await get(db_session=db_session, person_id=person_id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id `{person_id}` does not exist.",
        )

    person = await update(db_session=db_session, person=person, person_in=person_in)

    return person


@router.delete("/{person_id}", response_model=None)
async def delete_person(
    db_session: SessionDep, person_id: int, current_user: User = OwnerAdminManager
):
    """Delete a person."""
    person = await get(db_session=db_session, person_id=person_id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person with id `{person_id}` does not exist.",
        )
    await delete(db_session=db_session, person_id=person_id)
