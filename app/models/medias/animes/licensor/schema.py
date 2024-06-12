from pydantic import BaseModel, HttpUrl
from typing import Optional


class LicensorBase(BaseModel):
    name: str


class LicensorCreate(LicensorBase):
    url: Optional[HttpUrl] = None 
    

class LicensorCreateOrUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    url: Optional[HttpUrl] = None


class Licensor(LicensorBase):
    id: int

    class Config:
        orm_mode = True
