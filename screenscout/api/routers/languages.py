from fastapi import APIRouter, HTTPException, status

from screenscout.api.deps import SessionDep
from screenscout.crud.language import create, delete, get, get_all, get_by_name, update
from screenscout.schemas.language import LanguageCreate, LanguageRead, LanguageUpdate


router = APIRouter()


@router.get("/", response_model=list[LanguageRead])
async def get_languages(db_session: SessionDep):
    """Return all languages in the database."""
    return await get_all(db_session=db_session)


@router.get("/{language_id}", response_model=LanguageRead)
async def get_language(db_session: SessionDep, language_id: int):
    """Retrieve information about a language by its ID."""
    language = await get(db_session=db_session, language_id=language_id)
    if not language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Language with id `{language_id}` does not exist.",
        )

    return language


@router.post("/", response_model=LanguageRead)
async def create_language(db_session: SessionDep, language_in: LanguageCreate):
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
    db_session: SessionDep, language_id: int, language_in: LanguageUpdate
):
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
async def delete_language(db_session: SessionDep, language_id: int):
    """Delete a language."""
    language = await get(db_session=db_session, language_id=language_id)
    if not language:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Language with id `{language_id}` does not exist.",
        )
    await delete(db_session=db_session, language_id=language_id)
