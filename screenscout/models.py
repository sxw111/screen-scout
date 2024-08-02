from pydantic import BaseModel


# Pydantic models base class
class ScreenScoutBase(BaseModel):
    class Config:
        from_attributes = True


