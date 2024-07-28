from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from screenscout.models.user import User
from screenscout.schemas.user import UserCreate, UserUpdate
from screenscout.core.security import get_password_hash


async def get(*, db_session: AsyncSession, user_id) -> User | None:
    """Returns a user based on the given id."""
    result = await db_session.execute(select(User).where(User.id == user_id))

    return result.scalars().first()


async def get_all(*, db_session: AsyncSession) -> list[User | None]:
    """Return all users."""
    result = await db_session.execute(select(User))

    return result.scalars().all()


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
