from pydantic import BaseModel

class LanguageBase(BaseModel):
    name: str


class LanguageCreateOrUpdate(LanguageBase):
    pass

class Language(LanguageBase):
    id: int

    class Config:
        orm_mode = True
   


