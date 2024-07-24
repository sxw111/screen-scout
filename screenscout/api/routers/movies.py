from fastapi import APIRouter, HTTPException, status

from screenscout.api.deps import SessionDep
from screenscout.schemas.movie import MovieCreate, MovieRead, MovieUpdate
from screenscout.crud.movie import get, get_all, create, update, delete

router = APIRouter()


@router.get("/", response_model=list[MovieRead])
async def get_movies(db_session: SessionDep):
    """Return all movies in the database."""
    return await get_all(db_session=db_session)


@router.get("/{movie_id}", response_model=MovieRead)
async def get_movie(db_session: SessionDep, movie_id: int):
    """Retrieve information about a movie by its ID."""
    movie = await get(db_session=db_session, movie_id=movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with id `{movie_id}` does not exist.",
        )

    return movie


@router.post("/", response_model=MovieRead)
async def create_movie(db_session: SessionDep, movie_in: MovieCreate):
    """Create a new movie."""
    movie = await create(db_session=db_session, movie_in=movie_in)

    return movie


@router.put("/{movie_id}", response_model=MovieRead)
async def update_movie(db_session: SessionDep, movie_id: int, movie_in: MovieUpdate):
    """Update a movie."""
    movie = await get(db_session=db_session, movie_id=movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with id `{movie_id}` does not exist.",
        )

    movie = await update(db_session=db_session, movie=movie, movie_in=movie_in)

    return movie


@router.delete("/{movie_id}", response_model=None)
async def delete_movie(db_session: SessionDep, movie_id: int):
    """Delete a movie."""
    movie = await get(db_session=db_session, movie_id=movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with id `{movie_id}` does not exist.",
        )
    await delete(db_session=db_session, movie_id=movie_id)
