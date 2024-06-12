from pydantic import BaseModel, HttpUrl
from typing import Optional

class StudioBase(BaseModel):
    name: str


class StudioCreate(StudioBase):
    url: Optional[HttpUrl] = None 
 
    
class StudioCreateOrUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    url: Optional[HttpUrl] = None


class Studio(StudioBase):
    id: int

    class Config:
        orm_mode = True
