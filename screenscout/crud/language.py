from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from screenscout.models.language import Language
from screenscout.schemas.language import LanguageCreate, LanguageUpdate


async def get(*, db_session: AsyncSession, language_id: int) -> Language | None:
    """Returns a language based on the given id."""
    result = await db_session.execute(
        select(Language).where(Language.id == language_id)
    )

    return result.scalars().first()


async def get_by_name(*, db_session: AsyncSession, name: str) -> Language | None:
    """Returns a language by its name."""
    result = await db_session.execute(select(Language).where(Language.name == name))

    return result.scalars().first()


async def get_all(*, db_session: AsyncSession) -> list[Language | None]:
    """Return all languages."""
    result = await db_session.execute(select(Language))

    return result.scalars().all()


async def create(*, db_session: AsyncSession, language_in: LanguageCreate) -> Language:
    """Creates a new language."""
    language = Language(**language_in.model_dump())
    db_session.add(language)
    await db_session.commit()
    await db_session.refresh(language)

    return language


async def update(
    *, db_session: AsyncSession, language: Language, language_in: LanguageUpdate
) -> Language:
    """Updates a language."""
    language_data = language.dict()
    update_data = language_in.model_dump(exclude_unset=True)
    for field in language_data:
        if field in update_data:
            setattr(language, field, update_data[field])

    await db_session.commit()
    await db_session.refresh(language)

    return language


async def delete(*, db_session: AsyncSession, language_id: int):
    """Deletes an existing language."""
    result = await db_session.execute(
        select(Language).where(Language.id == language_id)
    )
    language = result.scalars().first()
    await db_session.delete(language)
    await db_session.commit()
