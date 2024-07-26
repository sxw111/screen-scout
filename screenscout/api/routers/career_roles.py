from fastapi import APIRouter, HTTPException, status

from screenscout.api.deps import SessionDep
from screenscout.crud.career_role import (
    create,
    delete,
    get,
    get_all,
    get_by_name,
    update,
)
from screenscout.schemas.career_role import (
    CareerRoleCreate,
    CareerRoleRead,
    CareerRoleUpdate,
)


router = APIRouter()


@router.get("/", response_model=list[CareerRoleRead])
async def get_career_roles(db_session: SessionDep):
    """Return all career roles in the database."""
    return await get_all(db_session=db_session)


@router.get("/{career_role_id}", response_model=CareerRoleRead)
async def get_career_role(db_session: SessionDep, career_role_id: int):
    """Retrieve information about a career role by its ID."""
    career_role = await get(db_session=db_session, career_role_id=career_role_id)
    if not career_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Career role with id `{career_role_id}` does not exist.",
        )

    return career_role


@router.post("/", response_model=CareerRoleRead)
async def create_career_role(db_session: SessionDep, career_role_in: CareerRoleCreate):
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
    db_session: SessionDep, career_role_id: int, career_role_in: CareerRoleUpdate
):
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
async def delete_career_role(db_session: SessionDep, career_role_id: int):
    """Delete a career role."""
    career_role = await get(db_session=db_session, career_role_id=career_role_id)
    if not career_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Career role with id `{career_role_id}` does not exist.",
        )
    await delete(db_session=db_session, career_role_id=career_role_id)
