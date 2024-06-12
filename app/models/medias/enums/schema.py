from typing import Optional
from pydantic import BaseModel, HttpUrl
from ...medias.enums_type import EnumsType
from ...medias.host import Host

class EnumsBase(BaseModel):
    name: str


class EnumsCreate(EnumsBase):
    url: Optional[HttpUrl] = None 
    
class EnumsCreateOrUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    url: Optional[HttpUrl] = None 
    site: Optional[Host] = None
    type: Optional[EnumsType] = None


class Enums(EnumsBase):
    site: Host
    type: EnumsType
    id: int

    class Config:
        orm_mode = True
