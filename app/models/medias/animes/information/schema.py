from pydantic import BaseModel
from typing import List, Optional
from ...enums.schema import EnumsCreate, EnumsCreateOrUpdate

class InformationBase(BaseModel):
    aired: Optional[str] = None
    episode: Optional[int] = None
    broadcast: Optional[str] = None

class InformationCreate(InformationBase):
    status: Optional[EnumsCreate] = None

class Information(InformationBase):
    id: int

    class Config:
        orm_mode = True
        
class InformationUpdate(InformationBase):
    status: Optional[EnumsCreateOrUpdate] = None
    
    
    
