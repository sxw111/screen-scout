from pydantic import BaseModel


class CareerRoleCreate(BaseModel):
    name: str


class CareerRoleRead(BaseModel):
    id: int
    name: str


class CareerRoleUpdate(BaseModel):
    name: str
