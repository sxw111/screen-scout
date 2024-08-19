from typing import Any

from fastapi import APIRouter, HTTPException, status
from fastapi_cache.decorator import cache

from screenscout.auth.models import User
from screenscout.auth.permissions import OwnerAdminManager
from screenscout.database.core import SessionDep

from .models import CareerRoleCreate, CareerRoleRead, CareerRoleUpdate
from .service import create, delete, get, get_all, get_by_name, update

router = APIRouter()


@router.get("/", response_model=list[CareerRoleRead])
@cache(expire=3600)
async def get_career_roles(
    db_session: SessionDep, current_user: User = OwnerAdminManager
) -> Any:
    """Return all career roles in the database."""
    return await get_all(db_session=db_session)


@router.get("/{career_role_id}", response_model=CareerRoleRead)
@cache(expire=3600)
async def get_career_role(
    db_session: SessionDep, career_role_id: int, current_user: User = OwnerAdminManager
) -> Any:
    """Retrieve information about a career role by its ID."""
    career_role = await get(db_session=db_session, career_role_id=career_role_id)
    if not career_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Career role with id `{career_role_id}` does not exist.",
        )

    return career_role


@router.post("/", response_model=CareerRoleRead, status_code=status.HTTP_201_CREATED)
async def create_career_role(
    db_session: SessionDep,
    career_role_in: CareerRoleCreate,
    current_user: User = OwnerAdminManager,
) -> Any:
    """Create a new career role."""
    career_role = await get_by_name(db_session=db_session, name=career_role_in.name)
    if career_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Career role with name `{career_role_in.name}` already exists.",
        )

    career_role = await create(db_session=db_session, career_role_in=career_role_in)

    return career_role


@router.put("/{career_role_id}", response_model=CareerRoleRead)
async def update_career_role(
    db_session: SessionDep,
    career_role_id: int,
    career_role_in: CareerRoleUpdate,
    current_user: User = OwnerAdminManager,
) -> Any:
    """Update a career role."""
    career_role = await get(db_session=db_session, career_role_id=career_role_id)
    if not career_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Career_role with id `{career_role_id}` does not exist.",
        )
    career_role = await update(
        db_session=db_session, career_role=career_role, career_role_in=career_role_in
    )

    return career_role


@router.delete("/{career_role_id}", response_model=None)
async def delete_career_role(
    db_session: SessionDep, career_role_id: int, current_user: User = OwnerAdminManager
) -> None:
    """Delete a career role."""
    career_role = await get(db_session=db_session, career_role_id=career_role_id)
    if not career_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Career role with id `{career_role_id}` does not exist.",
        )
    await delete(db_session=db_session, career_role_id=career_role_id)
