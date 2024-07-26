from pydantic import BaseModel


class CareerRoleBase(BaseModel):
    name: str


class CareerRoleCreate(CareerRoleBase):
    pass


class CareerRoleUpdate(CareerRoleCreate):
    pass


class CareerRoleRead(CareerRoleCreate):
    id: int
