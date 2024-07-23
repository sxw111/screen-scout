from fastapi import APIRouter, HTTPException, status

from screenscout.api.deps import SessionDep
from screenscout.schemas.genre import GenreCreate, GenreRead, GenreUpdate
from screenscout.crud.genre import get, get_all, create, update, delete, get_by_name


router = APIRouter()


@router.get("/", response_model=list[GenreRead])
async def get_genres(db_session: SessionDep):
    """Return all genres in the database."""
    return await get_all(db_session=db_session)


@router.get("/{genre_id}", response_model=GenreRead)
async def get_genre(db_session: SessionDep, genre_id: int):
    """Retrieve information about a genre by its ID."""
    genre = await get(db_session=db_session, genre_id=genre_id)
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genre with id `{genre_id}` does not exist.",
        )
    return genre


@router.post("/", response_model=GenreRead)
async def create_genre(db_session: SessionDep, genre_in: GenreCreate):
    """Create a new genre."""
    genre = await get_by_name(db_session=db_session, name=genre_in.name)
    if genre:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Genre with name `{genre_in.name}` already exists.",
        )

    genre = await create(db_session=db_session, genre_in=genre_in)

    return genre


@router.put("/{genre_id}", response_model=GenreRead)
async def update_genre(db_session: SessionDep, genre_id: int, genre_in: GenreUpdate):
    """Update a genre."""
    genre = await get(db_session=db_session, genre_id=genre_id)
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genre with id `{genre_id}` does not exist.",
        )
    genre = update(db_session=db_session, genre=genre, genre_in=genre_in)

    return genre


@router.delete("/{genre_id}", response_model=None)
async def delete_genre(db_session: SessionDep, genre_id: int):
    """Delete a genre."""
    genre = await get(db_session=db_session, genre_id=genre_id)
    if not genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Genre with id `{genre_id}` does not exist.",
        )
    await delete(db_session=db_session, genre_id=genre_id)
