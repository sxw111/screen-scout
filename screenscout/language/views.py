from typing import Any

from fastapi import APIRouter, HTTPException, status
from fastapi_cache.decorator import cache

from screenscout.auth.models import User
from screenscout.auth.permissions import OwnerAdminManager
from screenscout.database.core import SessionDep

from .models import LanguageCreate, LanguageRead, LanguageUpdate
from .service import create, delete, get, get_all, get_by_name, update

router = APIRouter()


@router.get("/", response_model=list[LanguageRead])
@cache(expire=3600)
async def get_languages(
    db_session: SessionDep, current_user: User = OwnerAdminManager
) -> Any:
    """Return all languages in the database."""
    return await get_all(db_session=db_session)


@router.get("/{language_id}", response_model=LanguageRead)
@cache(expire=3600)
async def get_language(
    db_session: SessionDep, language_id: int, current_user: User = OwnerAdminManager
) -> Any:
    """Retrieve information about a language by its ID."""
    language = await get(db_session=db_session, language_id=language_id)
    if not language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Language with id `{language_id}` does not exist.",
        )

    return language


@router.post("/", response_model=LanguageRead)
async def create_language(
    db_session: SessionDep,
    language_in: LanguageCreate,
    current_user: User = OwnerAdminManager,
) -> Any:
    """Create a new language."""
    language = await get_by_name(db_session=db_session, name=language_in.name)
    if language:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Language with name `{language_in.name}` already exists.",
        )

    language = await create(db_session=db_session, language_in=language_in)

    return language


@router.put("/{language_id}", response_model=LanguageRead)
async def update_language(
    db_session: SessionDep,
    language_id: int,
    language_in: LanguageUpdate,
    current_user: User = OwnerAdminManager,
) -> Any:
    """Update a language."""
    language = await get(db_session=db_session, language_id=language_id)
    if not language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Language with id `{language_id}` does not exist.",
        )
    language = await update(
        db_session=db_session, language=language, language_in=language_in
    )

    return language


@router.delete("/{language_id}", response_model=None)
async def delete_language(
    db_session: SessionDep, language_id: int, current_user: User = OwnerAdminManager
) -> None:
    """Delete a language."""
    language = await get(db_session=db_session, language_id=language_id)
    if not language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Language with id `{language_id}` does not exist.",
        )
    await delete(db_session=db_session, language_id=language_id)
