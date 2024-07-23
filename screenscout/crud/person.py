from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from screenscout.models.person import Person
from screenscout.models.career_role import CareerRole
from screenscout.models.genre import Genre
from screenscout.schemas.person import PersonCreate, PersonUpdate


async def get(*, db_session: AsyncSession, person_id: int) -> Person:
    """Returns a person based on the given id."""
    result = await db_session.execute(select(Person).where(Person.id == person_id))

    return result.scalars().first()


async def get_all(*, db_session: AsyncSession) -> list[Person | None]:
    """Return all persons."""
    result = await db_session.execute(select(Person))

    return result.scalars().all()


async def create(*, db_session: AsyncSession, person_in: PersonCreate) -> Person:
    """Creates a new person."""
    person = Person(**person_in.model_dump())
    db_session.add(person)
    await db_session.commit()
    await db_session.refresh(person)

    if person_in.career:
        for career_id in person_in.career:
            result = await db_session.execute(
                select(CareerRole).where(CareerRole.id == career_id)
            )
            career = result.scalars().first()
            if career:
                person.career.append(career)
        await db_session.commit()

    if person_in.genres:
        for genre_id in person_in.genres:
            result = await db_session.execute(select(Genre).where(Genre.id == genre_id))
            genre = result.scalars().first()
            if genre:
                person.genres.append(genre)
        await db_session.commit()

    return person


async def update(*, db_session: AsyncSession, person: Person, person_in: PersonUpdate) -> Person:
    """Updates a person."""
    person_data = person.dict()
    update_data = person_in.model_dump(skip_defaults=True)
    for field in person_data:
        if field in update_data:
            setattr(person, field, update_data[field])

    if person_in.career is not None:
        person.career.clear()
        for career_id in person_in.career:
            result = await db_session.execute(select(CareerRole).where(CareerRole.id == career_id))
            career = result.scalars().first()
            if career:
                person.career.append(career)

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