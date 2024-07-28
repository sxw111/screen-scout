from fastapi import APIRouter, HTTPException, status

from screenscout.api.deps import CurrentUser, SessionDep
from screenscout.crud.user import get, update
from screenscout.schemas.user import UserRead, UserUpdate


router = APIRouter()


@router.get("/me", response_model=UserRead)
async def get_me(current_user: CurrentUser):
    """Retrieve the current user's details."""
    return current_user


@router.get("/{user_id}", response_model=UserRead)
async def get_user(db_session: SessionDep, user_id: int):
    """Get a user."""
    user = await get(db_session=db_session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"A user with id `{user_id}` does not exist.",
        )

    return user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    db_session: SessionDep, current_user: CurrentUser, user_in: UserUpdate
):
    """Update a user."""
    user = await get(db_session=db_session, user_id=current_user.id)

    return await update(db_session=db_session, user=user, user_in=user_in)
