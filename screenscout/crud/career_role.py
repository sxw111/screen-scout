from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from screenscout.models.career_role import CareerRole
from screenscout.schemas.career_role import CareerRoleCreate, CareerRoleUpdate


async def get(*, db_session: AsyncSession, career_role_id: int) -> CareerRole | None:
    """Returns a career role based on the given id."""
    result = await db_session.execute(
        select(CareerRole).where(CareerRole.id == career_role_id)
    )

    return result.scalars().first()


async def get_by_name(*, db_session: AsyncSession, name: str) -> CareerRole | None:
    """Returns a career role by its name."""
    result = await db_session.execute(select(CareerRole).where(CareerRole.name == name))

    return result.scalars().first()


async def get_all(*, db_session: AsyncSession) -> list[CareerRole | None]:
    """Return all career roles."""
    result = await db_session.execute(select(CareerRole))

    return result.scalars().all()


async def create(
    *, db_session: AsyncSession, career_role_in: CareerRoleCreate
) -> CareerRole:
    """Creates a new career role."""
    career_role = CareerRole(**career_role_in.model_dump())
    db_session.add(career_role)
    await db_session.commit()
    await db_session.refresh(career_role)

    return career_role


async def update(
    *,
    db_session: AsyncSession,
    career_role: CareerRole,
    career_role_in: CareerRoleUpdate
) -> CareerRole:
    """Updates a career role."""
    career_role_data = career_role.dict()
    update_data = career_role_in.model_dump(skip_defaults=True)
    for field in career_role_data:
        if field in update_data:
            setattr(career_role, field, update_data[field])

    await db_session.commit()
    await db_session.refresh(career_role)

    return career_role


async def delete(*, db_session: AsyncSession, career_role_id: int):
    """Deletes an existing career role."""
    result = await db_session.execute(
        select(CareerRole).where(CareerRole.id == career_role_id)
    )
    career_role = result.scalars().first()
    await db_session.delete(career_role)
    await db_session.commit()
