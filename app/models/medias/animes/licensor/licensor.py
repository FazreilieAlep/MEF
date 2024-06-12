from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .....core.database import Base
from ...associations import anime_licensors

class Licensor(Base):
    __tablename__ = "licensors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=True)
    
    licensed = relationship("Anime", secondary=anime_licensors, back_populates="licensors")