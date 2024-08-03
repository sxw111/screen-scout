from fastapi import APIRouter

from screenscout.auth.views import auth_router, users_router
from screenscout.career_role.views import router as career_roles_router
from screenscout.country.views import router as countries_router
from screenscout.genre.views import router as genres_router
from screenscout.language.views import router as languages_router
from screenscout.movie.views import router as movies_router
from screenscout.person.views import router as persons_router
from screenscout.series.views import router as series_router
from screenscout.watchlist.views import router as watchlist_router
from screenscout.movie_list.views import router as movie_lists_router
from screenscout.series_list.views import router as series_lists_router


api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(countries_router, prefix="/countries", tags=["countries"])
api_router.include_router(languages_router, prefix="/languages", tags=["languages"])
api_router.include_router(genres_router, prefix="/genres", tags=["genres"])
api_router.include_router(
    career_roles_router, prefix="/career_roles", tags=["career_roles"]
)
api_router.include_router(movies_router, prefix="/movies", tags=["movies"])
api_router.include_router(series_router, prefix="/series", tags=["series"])
api_router.include_router(persons_router, prefix="/persons", tags=["persons"])
api_router.include_router(watchlist_router, prefix="/watchlist", tags=["watchlist"])
api_router.include_router(
    movie_lists_router, prefix="/lists/movies", tags=["movie lists"]
)
api_router.include_router(
    series_lists_router, prefix="/lists/series", tags=["series lists"]
)


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}
