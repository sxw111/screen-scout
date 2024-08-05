from fastapi import HTTPException, status


class EntityDoesNotExist(Exception):
    """
    Data does not exist in the database.
    """


class EntityAlreadyExists(Exception):
    """
    Data already exists in the database.
    """


class CredentialsException(HTTPException):
    """
    Exception raised when credentials could not be validated.
    """

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserDeactivatedException(HTTPException):
    """
    Exception raised when a user account is deactivated.
    """

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated",
        )
