from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from screenscout.core.config import settings

DATABASE_URL = (
    "postgresql+asyncpg://"
    f"{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/"
    f"{settings.POSTGRES_DB}"
)

async_engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models.

    All other models should inherit from this class.
    """

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
