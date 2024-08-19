from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from screenscout.database.core import SessionDep
from screenscout.jwt.models import TokenResponse
from screenscout.security import create_access_token, verify_password

from .models import UserCreate, UserRead, UserUpdate
from .service import CurrentUser, create, get, get_by_email, get_by_username, update

auth_router = APIRouter()
users_router = APIRouter()


@auth_router.post(
    "/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED
)
async def signup(db_session: SessionDep, user_in: UserCreate) -> Any:
    """Creates a new user account."""
    user = await get_by_email(db_session=db_session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email `{user_in.email}` already exists.",
        )

    user = await get_by_username(db_session=db_session, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with username `{user_in.username}` already exists.",
        )

    user = await create(db_session=db_session, user_in=user_in)

    return user


@auth_router.post("/signin")
async def signin(
    db_session: SessionDep, user_credentials: OAuth2PasswordRequestForm = Depends()
) -> TokenResponse:
    """Authenticates a user and provides an access token."""
    user = await get_by_email(db_session=db_session, email=user_credentials.username)

    if user and verify_password(user_credentials.password, user.password):
        data = {
            "user_id": user.id,
            "role": user.role,
        }
        access_token = create_access_token(data=data)

        return TokenResponse(access_token=access_token, token_type="bearer")

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password.",
        headers={"WWW-Authenticate": "Bearer"},
    )


@users_router.get("/me", response_model=UserRead)
async def get_me(current_user: CurrentUser) -> Any:
    """Retrieve the current user's details."""
    return current_user


@users_router.get("/{user_id}", response_model=UserRead)
async def get_user(db_session: SessionDep, user_id: int) -> Any:
    """Get a user."""
    user = await get(db_session=db_session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"A user with id `{user_id}` does not exist.",
        )

    return user


@users_router.put("/{user_id}", response_model=UserRead)
async def update_user(
    db_session: SessionDep, current_user: CurrentUser, user_in: UserUpdate
) -> Any:
    """Update a user."""
    user = await get(db_session=db_session, user_id=current_user.id)

    return await update(
        db_session=db_session, user=user, user_in=user_in
    )  # type: ignore
