from fastapi import HTTPException, Depends
from functools import wraps

from .enums import UserRole
from .service import get_current_user
from .models import User


def role_required(roles: list[UserRole]):
    def decorator(func: callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user: User = await get_current_user(*args, **kwargs)
            if user.role not in roles:
                raise HTTPException(
                    status_code=403,
                    detail="You do not have permission to access this resource",
                )

            return await func(*args, **kwargs, user=user)

        return wrapper

    return decorator


