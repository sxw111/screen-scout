from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from screenscout.api.deps import SessionDep, CurrentUser
from screenscout.crud.user import (
    create,
    get,
    get_all,
    get_by_email,
    get_by_username,
    update,
)
from screenscout.core.security import verify_password, create_access_token
from screenscout.schemas.user import UserCreate, UserRead, UserUpdate
from screenscout.schemas.jwt_token import TokenResponse


router = APIRouter()


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


@router.get("/me", response_model=UserRead)
async def get_me(db_session: SessionDep, current_user: CurrentUser):
    """Retrieve the current user's details."""
    return await get(db_session=db_session, user_id=current_user.id)


@router.put("/{user_id}")
async def update_user(
    db_session: SessionDep, current_user: CurrentUser, user_in: UserUpdate
):
    """Update a user."""
    user = await get(db_session=db_session, user_id=current_user.id)

    return await update(db_session=db_session, user=user, user_in=user_in)
