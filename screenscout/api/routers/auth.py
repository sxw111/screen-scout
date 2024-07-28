from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from screenscout.api.deps import SessionDep
from screenscout.crud.user import create, get_by_email, get_by_username
from screenscout.core.security import verify_password, create_access_token
from screenscout.schemas.user import UserCreate, UserRead
from screenscout.schemas.jwt_token import TokenResponse


router = APIRouter()


@router.post("/signup", response_model=UserRead)
async def signup(db_session: SessionDep, user_in: UserCreate):
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


@router.post("/signin")
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
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
