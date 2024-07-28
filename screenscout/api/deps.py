from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from screenscout.core.config import settings
from screenscout.core.db import async_session
from screenscout.models.user import User
from screenscout.schemas.jwt_token import TokenData


oauth2_scheme_v1 = OAuth2PasswordBearer(tokenUrl="api/v1/auth/signin")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]


async def verify_access_token(token: str, credentials_exception) -> TokenData:
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


async def get_current_user(
    db: SessionDep, token: Annotated[str, Depends(oauth2_scheme_v1)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = await verify_access_token(token, credentials_exception)

    result = await db.execute(select(User).where(User.id == token_data.id))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    if user.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )

    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
