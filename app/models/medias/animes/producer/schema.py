from pydantic import BaseModel, HttpUrl
from typing import Optional


class ProducerBase(BaseModel):
    name: str


class ProducerCreate(ProducerBase):
    url: Optional[HttpUrl] = None
    

class ProducerCreateOrUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    url: Optional[HttpUrl] = None


class Producer(ProducerBase):
    id: int

    class Config:
        orm_mode = True
