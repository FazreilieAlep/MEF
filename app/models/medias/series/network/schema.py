from pydantic import BaseModel

class NetworkBase(BaseModel):
    name: str


class NetworkCreateOrUpdate(NetworkBase):
    pass

class Network(NetworkBase):
    id: int

    class Config:
        orm_mode = True
   


