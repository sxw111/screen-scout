from pydantic import BaseModel


class LanguageBase(BaseModel):
    name: str


class LanguageCreate(LanguageBase):
    pass


class LanguageUpdate(LanguageBase):
    pass


class LanguageRead(LanguageBase):
    id: int
