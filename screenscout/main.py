from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from starlette.middleware.cors import CORSMiddleware

from screenscout.auth.service import first_owner_create
from screenscout.database.core import get_db

from .api import api_router
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Startup
    async for db_session in get_db():
        await first_owner_create(db_session)

    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    # Shutdown


# Initialize a FastAPI application with custom settings
app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    docs_url=settings.DOCS_URL,
    openapi_url=settings.OPENAPI_URL,
    redoc_url=settings.REDOC_URL,
    lifespan=lifespan,
)

# Add CORS middleware to the FastAPI application
# This middleware allows configuring how the server
# should respond to cross-origin requests.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)
