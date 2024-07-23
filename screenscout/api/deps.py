from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from screenscout.core.db import async_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]
