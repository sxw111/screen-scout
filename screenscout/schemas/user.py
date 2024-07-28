from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    username: str | None
    email: EmailStr | None
    password: str | None


class UserRead(UserBase):
    id: int
