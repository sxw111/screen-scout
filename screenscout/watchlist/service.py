from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import union_all

from screenscout.auth.models import User

from screenscout.movie.models import Movie
from screenscout.series.models import Series
from screenscout.auth.service import get as get_user
from screenscout.movie.service import get as get_movie
from screenscout.exceptions import EntityDoesNotExist, EntityAlreadyExists


async def create_movie_watchlist_item(): ...
