from pydantic import BaseModel

class CountryBase(BaseModel):
    name: str


class CountryCreateOrUpdate(CountryBase):
    pass

class Country(CountryBase):
    id: int

    class Config:
        orm_mode = True
   


