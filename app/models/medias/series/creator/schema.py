from pydantic import BaseModel

class CreatorBase(BaseModel):
    name: str


class CreatorCreateOrUpdate(CreatorBase):
    pass

class Creator(CreatorBase):
    id: int

    class Config:
        orm_mode = True
   


