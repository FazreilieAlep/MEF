from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .....core.database import Base
from ...associations import anime_producers

class Producer(Base):
    __tablename__ = "producers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=True)
    
    produced = relationship("Anime", secondary=anime_producers, back_populates="producers")
    