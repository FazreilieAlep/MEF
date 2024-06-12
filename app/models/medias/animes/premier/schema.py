from pydantic import BaseModel, HttpUrl
from typing import Optional


class PremierBase(BaseModel):
    name: str

class PremierCreate(PremierBase):
    url: Optional[HttpUrl] = None
    

class PremierCreateOrUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    url: Optional[HttpUrl] = None


class Premier(PremierBase):
    id: int

    class Config:
        orm_mode = True
