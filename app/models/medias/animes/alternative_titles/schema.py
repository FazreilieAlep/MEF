from pydantic import BaseModel, HttpUrl
from typing import Optional


class AlternativeTitlesBase(BaseModel):
    synonym: Optional[str] = None
    japanese: Optional[str] = None


class AlternativeTitlesCreate(AlternativeTitlesBase):
    pass

class AlternativeTitlesUpdate(AlternativeTitlesBase):
    pass

class AlternativeTitles(AlternativeTitlesBase):
    id: int

    class Config:
        orm_mode = True
