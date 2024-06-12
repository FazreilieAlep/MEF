from pydantic import BaseModel

class StarBase(BaseModel):
    name: str

class StarCreateOrUpdate(StarBase):
    pass

class Star(StarBase):
    id: int

    class Config:
        orm_mode = True
   


