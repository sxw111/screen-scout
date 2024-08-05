from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from screenscout.config import settings
from screenscout.database.core import SessionDep
from screenscout.exceptions import CredentialsException, UserDeactivatedException
from screenscout.jwt.models import TokenData
from screenscout.security import get_password_hash

from .models import User, UserCreate, UserUpdate


async def get(*, db_session: AsyncSession, user_id: int) -> User | None:
    """Returns a user based on the given id."""
    result = await db_session.execute(select(User).where(User.id == user_id))

    return result.scalars().first()


async def get_all(*, db_session: AsyncSession) -> list[User]:
    """Return all users."""
    result = await db_session.execute(select(User))

    return result.scalars().all()  # type: ignore


async def get_by_email(*, db_session: AsyncSession, email: EmailStr) -> User | None:
    """Returns a user by its email."""
    query = select(User).where(User.email == email)

    result = await db_session.execute(query)

    return result.scalars().first()


async def get_by_username(*, db_session: AsyncSession, username: str) -> User | None:
    """Returns a user by its username."""
    query = select(User).where(User.username == username)

    result = await db_session.execute(query)

    return result.scalars().first()


async def create(*, db_session: AsyncSession, user_in: UserCreate) -> User:
    """Creates a new user."""
    hashed_password = get_password_hash(user_in.password)
    user_in.password = hashed_password

    user = User(**user_in.model_dump())
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    return user


async def update(*, db_session: AsyncSession, user: User, user_in: UserUpdate) -> User:
    """Updates a user."""
    user_data = user.dict()
    update_data = user_in.model_dump(exclude={"password"}, exclude_unset=True)

    for field in user_data:
        if field in update_data:
            setattr(user, field, update_data[field])

    if user_in.password:
        hashed_password = get_password_hash(user_in.password)
        user.password = hashed_password

    await db_session.commit()
    await db_session.refresh(user)

    return user


async def verify_access_token(
    token: str, credentials_exception: CredentialsException
) -> TokenData:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data


oauth2_scheme_v1 = OAuth2PasswordBearer(tokenUrl="api/v1/auth/signin")


async def get_current_user(
    db: SessionDep, token: Annotated[str, Depends(oauth2_scheme_v1)]
) -> User:
    token_data = await verify_access_token(token, CredentialsException())

    result = await db.execute(select(User).where(User.id == token_data.id))
    user = result.scalars().first()

    if user is None:
        raise CredentialsException()

    if user.is_active is False:
        raise UserDeactivatedException()

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
