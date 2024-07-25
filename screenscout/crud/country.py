from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from screenscout.models.country import Country
from screenscout.schemas.country import CountryCreate, CountryUpdate


async def get(*, db_session: AsyncSession, country_id: int) -> Country | None:
    """Returns a country based on the given id."""
    result = await db_session.execute(select(Country).where(Country.id == country_id))

    return result.scalars().first()


async def get_by_name(*, db_session: AsyncSession, name: str) -> Country | None:
    """Returns a country by its name."""
    result = await db_session.execute(select(Country).where(Country.name == name))

    return result.scalars().first()


async def get_all(*, db_session: AsyncSession) -> list[Country | None]:
    """Return all countries."""
    result = await db_session.execute(select(Country))

    return result.scalars().all()


async def create(*, db_session: AsyncSession, country_in: CountryCreate) -> Country:
    """Creates a new country."""
    country = Country(**country_in.model_dump())
    db_session.add(country)
    await db_session.commit()
    await db_session.refresh(country)

    return country


async def update(
    *, db_session: AsyncSession, country: Country, country_in: CountryUpdate
) -> Country:
    """Updates a country."""
    country_data = country.dict()
    update_data = country_in.model_dump(exclude_unset=True)
    for field in country_data:
        if field in update_data:
            setattr(country, field, update_data[field])

    await db_session.commit()
    await db_session.refresh(country)

    return country


async def delete(*, db_session: AsyncSession, country_id: int):
    """Deletes an existing country."""
    result = await db_session.execute(select(Country).where(Country.id == country_id))
    country = result.scalars().first()
    await db_session.delete(country)
    await db_session.commit()
