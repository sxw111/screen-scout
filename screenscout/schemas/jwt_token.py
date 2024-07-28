from pydantic import BaseModel


class TokenData(BaseModel):
    id: int | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
