from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api import api_router
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup
    yield
    # Shutdown


# Initialize a FastAPI application with custom settings
app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    docs_url=settings.DOCS_URL,
    openapi_url=settings.OPENAPI_URL,
    redoc_url=settings.REDOC_URL,
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
