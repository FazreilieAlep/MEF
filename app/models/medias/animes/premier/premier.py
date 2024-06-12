from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .....core.database import Base

class Premier(Base):
    __tablename__ = "premiers"
    
    id = Column(Integer, primary_key=True) 
    name = Column(String, nullable=False)
    url = Column(String, nullable=True)
    
    anime = relationship("Anime", back_populates="premiered")