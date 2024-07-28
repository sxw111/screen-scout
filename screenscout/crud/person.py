from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from screenscout.models.person import Person
from screenscout.models.career_role import CareerRole
from screenscout.models.genre import Genre
from screenscout.schemas.person import PersonCreate, PersonUpdate


async def get(*, db_session: AsyncSession, person_id: int) -> Person | None:
    """Returns a person based on the given id."""
    query = (
        select(Person)
        .where(Person.id == person_id)
        .options(selectinload(Person.genres), selectinload(Person.career_roles))
    )
    result = await db_session.execute(query)

    return result.scalars().first()


async def get_all(*, db_session: AsyncSession) -> list[Person | None]:
    """Return all persons."""
    query = select(Person).options(
        selectinload(Person.genres), selectinload(Person.career_roles)
    )
    result = await db_session.execute(query)

    return result.scalars().all()


async def create(*, db_session: AsyncSession, person_in: PersonCreate) -> Person:
    """Creates a new person."""
    person_data = person_in.model_dump()
    career_roles = person_data.pop("career_roles")
    genres = person_data.pop("genres")
    person = Person(**person_data)
    db_session.add(person)
    await db_session.commit()
    await db_session.refresh(person, ["career_roles", "genres"])

    for career_role_id in career_roles:
        result = await db_session.execute(
            select(CareerRole).where(CareerRole.id == career_role_id)
        )
        career_role = result.scalars().first()
        if career_role:
            db_session.add(career_role)
        person.career_roles.append(career_role)

    for genre_id in genres:
        result = await db_session.execute(select(Genre).where(Genre.id == genre_id))
        genre = result.scalars().first()
        if genre:
            db_session.add(genre)
        person.genres.append(genre)

    await db_session.commit()

    return person


async def update(
    *, db_session: AsyncSession, person: Person, person_in: PersonUpdate
) -> Person:
    """Updates a person."""
    person_data = person.dict()
    update_data = person_in.model_dump(exclude_unset=True)
    for field in person_data:
        if field in update_data:
            setattr(person, field, update_data[field])

    if person_in.career_roles is not None:
        person.career_roles.clear()
        for career_role_id in person_in.career_roles:
            result = await db_session.execute(
                select(CareerRole).where(CareerRole.id == career_role_id)
            )
            career_role = result.scalars().first()
            if career_role:
                person.career_roles.append(career_role)

    if person_in.genres is not None:
        person.genres.clear()
        for genre_id in person_in.genres:
            result = await db_session.execute(select(Genre).where(Genre.id == genre_id))
            genre = result.scalars().first()
            if genre:
                person.genres.append(genre)

    await db_session.commit()
    await db_session.refresh(person)

    return person


async def delete(*, db_session: AsyncSession, person_id: int):
    """Deletes an existing person."""
    result = await db_session.execute(select(Person).where(Person.id == person_id))
    person = result.scalars().first()
    await db_session.delete(person)
    await db_session.commit()
