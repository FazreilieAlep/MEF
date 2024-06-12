from pydantic import BaseModel

class ProductionBase(BaseModel):
    name: str


class ProductionCreateOrUpdate(ProductionBase):
    pass

class Production(ProductionBase):
    id: int

    class Config:
        orm_mode = True
   


