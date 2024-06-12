from typing import Optional
from pydantic import BaseModel

class ItemListResponse(BaseModel):
    id: int
    name: Optional[str] = None
    value: Optional[str] = None

    class Config:
        orm_mode = True
        
class ItemCreate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None