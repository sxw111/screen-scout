from screenscout.models import ScreenScoutBase


class TokenData(ScreenScoutBase):
    id: int | None = None


class TokenResponse(ScreenScoutBase):
    access_token: str
    token_type: str
