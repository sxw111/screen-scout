from fastapi import APIRouter

from screenscout.api.routers.auth import router as auth_router
from screenscout.api.routers.users import router as users_router
from screenscout.api.routers.career_roles import router as career_roles_router
from screenscout.api.routers.countries import router as countries_router
from screenscout.api.routers.genres import router as genres_router
from screenscout.api.routers.movies import router as movies_router
from screenscout.api.routers.persons import router as persons_router
from screenscout.api.routers.languages import router as languages_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(
    career_roles_router, prefix="/career_roles", tags=["career_roles"]
)
api_router.include_router(countries_router, prefix="/countries", tags=["countries"])
api_router.include_router(genres_router, prefix="/genres", tags=["genres"])
api_router.include_router(movies_router, prefix="/movies", tags=["movies"])
api_router.include_router(persons_router, prefix="/persons", tags=["persons"])
api_router.include_router(languages_router, prefix="/languages", tags=["languages"])


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}
