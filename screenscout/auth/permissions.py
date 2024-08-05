"""
Module for role-based access control.

This module provides utilities for enforcing role-based access control
in the application. It includes a decorator for checking user roles
and predefined dependencies for common role sets.

Roles:
- Owner: Has all permissions, including managing users, content, and other settings.
- Admin: Can manipulate users and perform other administrative tasks.
- Manager: Manages content such as movies, series, and personas.
- Member: Regular user with basic permissions.

Functions:
- `role_required`: Creates a dependency that ensures the current user
  has one of the required roles.
- `Owner`: Dependency for users with the OWNER role.
- `OwnerAdmin`: Dependency for users with either the OWNER or ADMIN role.
- `OwnerAdminManager`: Dependency for users with either the OWNER,
  ADMIN, or MANAGER role.
- `OwnerAdminManagerMember`: Dependency for users with any of the roles:
  OWNER, ADMIN, MANAGER, or MEMBER.
"""

from typing import Callable

from fastapi import Depends, HTTPException, status

from .enums import UserRole
from .models import User
from .service import get_current_user


def role_required(required_roles: list[UserRole]) -> Callable[[User], User]:
    """
    Decorator to check the user's role.

    This decorator is used to verify if the current user has one of the required roles.
    If the user's role is not in the list of allowed roles, it raises an HTTP 403
    Forbidden exception.
    """

    def role_checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return user

    return role_checker


# Define dependencies for different role sets
Owner = Depends(role_required([UserRole.OWNER]))

OwnerAdmin = Depends(role_required([UserRole.OWNER, UserRole.ADMIN]))

OwnerAdminManager = Depends(
    role_required([UserRole.OWNER, UserRole.ADMIN, UserRole.MANAGER])
)

OwnerAdminManagerMember = Depends(
    role_required([UserRole.OWNER, UserRole.ADMIN, UserRole.MANAGER, UserRole.MEMBER])
)
