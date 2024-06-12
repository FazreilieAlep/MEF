from pydantic import BaseModel

class DirectorBase(BaseModel):
    name: str


class DirectorCreateOrUpdate(DirectorBase):
    pass

class Director(DirectorBase):
    id: int

    class Config:
        orm_mode = True
   


